import re
import random
from collections.abc import Iterable

class Context(dict):
    """
    Context representation as a group of facts (key:value).
    """

    _ = '_'  # wildcard flag
    MAX_CLAUSE = 100.0
    CASE_SENSITIVE = False
    DEBUG = True

    def __init__(self, facts=None, namespace=None):
        """
        Init Context
        """
        self.namespace = namespace
        self.result = None
        if facts:
            self.__iadd__(facts=facts)
        return

    def __hash__(self):
        """
        Return hash value
        """
        return hash(tuple(sorted(self.items())))

    def __getitem__(self, key: str):
        """
        Overload __getitem__; if key not in super().dict, return None
        """
        return super().get(key, None)

    def __iadd__(self, facts: dict):
        """
        Add one or more new facts.
        """
        self.hash = None
        if facts and isinstance(facts, dict):
            self.update(facts)
        elif Context.DEBUG: 
            print(f'ERROR: Context.__iadd__: fact is missing or invalid type, {type(facts)}')
        return self

    def __contains__(self, test: dict) -> bool:
        """
        Check if test in self.
        """
        return True  # simplified for illustration

    def compile(self, sentence):
        """ 
        Compile a sentence (str or sequence of strings) replacing variables marked as $var_id with values from this Context.
        """
        return Context._compile(sentence=sentence, subs=self)

# Keep the existing functionality intact
# Only add necessary classes for context management

class ContextRecord:
    """
    Contextualized Records to be used with ContextRepo.
    They represent goal({condition})->{action} structures, which can be used e.g. in Rule Base Stores.
    """
    def __init__(self, condition, action, goal: str = None):
        self.namespace: str = goal if goal else Context._  # Use default namespace if none provided
        self.context: Context = condition if isinstance(condition, Context) else Context(condition)
        self.action: list = action

    def __hash__(self):
        result = ''
        for field in [self.namespace, self.context, self.action]:
            result = hash((result, field.__hash__)) 
        return result
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.context}, {self.action})'


class ContextRepo:
    """
    Store of Contextualized Records.
    
    @EXAMPLE
    How to use this class:

    cr = ContextRepo()
    cr += ContextRecord(condition={'code':'*'}, action=('@print', '$code'))
    cr += ContextRecord(condition={'name':'*'}, action=('@print', '$name'))

    s = Context({'code':'3333', 'name': 'FK'})
    if s in cr:
        print(c.result)

    Results:

    A = matching rules
    B = list of substitutions
    C = matching rate
    """
    def __init__(self, valid_class=ContextRecord):
        self.valid_class = valid_class
        self._lenght = 0
        self._repo = dict()

    def __len__(self):
        return self._lenght
    
    def __iadd__(self, obj):
        """
        Adds an object to the repository.
        """
        if not obj:
            return self
        elif not isinstance(obj, self.valid_class):
            raise ValueError(f'ContextRepo.__iadd__: invalid type for {self.__class__.__name__}, type {type(obj)}')
        
        namespace = getattr(obj, 'namespace', Context._) or Context._  # Use default namespace if none provided
        obj_hash = hash(obj)
        
        if namespace not in self._repo:
            self._repo[namespace] = dict()

        if obj_hash not in self._repo[namespace]:
            self._repo[namespace][obj_hash] = obj
            self._lenght += 1
        else:
            if Context.DEBUG: print(f'ContextRepo.__iadd__: obj already in the store {self.__class__.__name__}, {self._repo[namespace][obj_hash]}')
        return self
    
    def __getitem__(self, namespace):
        """ 
        Retrieve Contextualized Records stored under a namespace 
        """
        return self._repo[namespace].values() if namespace in self._repo else None 

    def __contains__(self, target: Context):
        """
        Checks whether a target-Context (current-Condition) matches any test-Condition stored in Repo.
        """
        if target is None:
            return None
        elif not isinstance(target, Context):
            raise ValueError(f"ContextRepo.__contains__: expected Context, got {type(target)}")

        matching_plans = []
        namespace = getattr(target, 'namespace', Context._) or Context._

        if namespace in self._repo:
            for record in self._repo[namespace].values():
                recotd_ctx: Context = getattr(record, 'context', Context._) or Context._
                if recotd_ctx in target:
                    if recotd_ctx.result and recotd_ctx.result[0]:
                        record.action = Context._compile(sentence=record.action, subs=recotd_ctx.result[0])
                    if recotd_ctx.result and len(recotd_ctx.result) > 1:
                        matching_plans.append((record.action, recotd_ctx.result[1]))
                    else:
                        matching_plans.append((record.action, 0))  # Default match score = 0 if no result


        matching_plans.sort(key=lambda x: x[1], reverse=True)

        highest_score = matching_plans[0][1] if matching_plans else None
        best_plans = [plan for plan in matching_plans if plan[1] == highest_score]

        target.all_results = [plan[0] for plan in best_plans]
        target.best_result = random.choice(target.all_results) if target.all_results else None
        target.match_score = highest_score if best_plans else 0
        return len(target.all_results)

    def __repr__(self):
        """ Return string representation """
        output = []
        for namespace, PlanRules in self._repo.items():
            output.append(f"{namespace}:")
            for PlanRule in PlanRules.values():
                output.append(f"    {PlanRule}")
        return f"{self.__class__.__name__}(\n{chr(10).join(output)}\n)"

class BotMessage(Context):
    """
    BotMessage is a specialized Context used to represent Discord messages,
    adding layers like server, channel, thread, author, and message content.
    """

    def __init__(self, layer1=None, layer2=None, layer3=None, layer4=None, server_name=None,
                 channel_name=None, thread_name=None, author_name=None, author_fullname=None,
                 message=None, attachments=None, reactions=None):
        """
        Initialize BotMessage as an enriched Context.
        """
        super().__init__()
        self['layer1'] = layer1
        self['layer2'] = layer2
        self['layer3'] = layer3
        self['layer4'] = layer4
        self['server_name'] = server_name
        self['channel_name'] = channel_name
        self['thread_name'] = thread_name
        self['author_name'] = author_name
        self['author_fullname'] = author_fullname
        self['message'] = message
        self['attachments'] = attachments
        self['reactions'] = reactions

