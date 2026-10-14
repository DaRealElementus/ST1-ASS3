# AI Usage Log

Format follows `checklist.md`: prompt, output summary, human check, Accept/Modify/Reject, reason, link.

## Entry 1: Dunder methods for SmartCare classes

| Field | Detail |
|---|---|
| Date | 2026-10-14 |
| Owner | Alex Larkings (AL) |
| Tool | Claude Code (Claude Opus 5.5), VS Code extension |
| Files affected | `project/smartcare/domain.py` |
| Branch / commit | `QOL-DunderMethods` / `c432838` |

### Conversation summary

| # | My prompt | AI output summary | My check / takeaway | Decision |
|---|---|---|---|---|
| 1 | Asked whether dunder methods could be used in `services.py` and whether they would help. | The service classes just coordinate calls, so only `__init__` is meaningful there. Suggested `__repr__` on domain classes. Advised against ID-based `__eq__`/`__hash__`, since that could hide a "replacement object" bug that the Stage 6 spec forbids, and objects are mutable. Suggested an explicit `sorted(key=...)` over `__lt__` for Stage 9. | Read `services.py` and `domain.py` to confirm the services only delegate to the store. | Accept the advice not to add dunders to services |
| 2 | Asked about `__int__`, `__dict__` or `__list__` to retrieve data "when the typing calls for it". | Explained that type hints never trigger conversions at runtime. `__int__` only runs on an explicit `int(x)`. `__dict__` is the instance attribute namespace, not a conversion hook. There is no `__list__` (`list(x)` uses `__iter__`). The store holds three collections, so `list(store)` would be ambiguous. | Corrected my misunderstanding that annotations call conversion methods. Kept the named store methods (`list_appointments()` etc.). | Reject my original idea |
| 3 | Asked what other dunder methods exist. | Gave an overview grouped by purpose (representation, comparison/hashing, containers, truthiness, attribute access, context managers, callables, arithmetic), with whether each fits this project. Recommended `__repr__` and optional `__str__` only. | Considered each group against our classes; agreed the rest have no natural meaning for Patient/Practitioner/Appointment. | Accept `__repr__` + `__str__` |
| 4 | Asked for the change on a new branch `QOL-DunderMethods`. | Added `__repr__` and `__str__` to `Patient`, `Practitioner` and `Appointment`. Appointment `__repr__` shows participants by ID to stay short. | Ran a manual print check of all three classes. Full test suite: 8 passed. Lines under 80 chars. Reviewed the diff before commit. | Accept |

### Rejected / not adopted

- `__eq__` / `__hash__` by ID: could mask Stage 6 "must not create a replacement" bugs; mutable objects.
- `__lt__` on Appointment: an explicit sort key in Stage 9 is clearer.
- `__int__`, `__dict__` override, container dunders on the store: no clear meaning; ambiguous across three collections.

### Reflection

I considered dunder methods for automatic calling/typing, Claude informed me that this wouldn't work and that each instance of this would have to be explicitly converted using the correct call (```str(), int(), list()```) inside the call.

I expected type hinting to FORCE a function to accept a certain type of value by either converting it or raising an error if the method wasn't implemented.

```py
class Bar():
    def __init__(self):
        self.text = "Lorem Ipsum"
        self.data = 12345678
    def __str__(self): # called at foo call
        return self.text

def foo(bar:str) -> bool: #bar gets turned into Lorem Ipsum here
    return bar == "Lorem Ipsum"

bar = Bar()
foo(bar) #True
```

However, I then learnt that Python doesn't do that, and instead the real implementation is

```py
# assume code above extends here

foo(str(bar)) # this is how it actually works, you have to call the explicit converter func
foo(bar) # returns false due to the object not eq to Lorem Ipsum, doesn't even raise error
```

This is just an example, but the ```__eq__``` could cause problems where a replacement patient could be returned, which goes against spec. Added in with the fact it would break hashing and make the objects mutable again.

The ```__str__``` and ```__repr__``` methods are simple to implement, just repetitive and even tedious at times, so I got AI to do the job.

Don't worry, I still checked and reviewed the output, this is just dunder methods that are minimally used (errors debugging etc, but have no effect on runtime code), but they still matter.

I don't think this changes the initial approach, this was meant to be a QOL feature, not a needed one, this PR might not be merged, but it would change how a GUI or error system would work, I need to recheck the checklist and see if they are under my domain of work.

### Link

[PR2](https://github.com/DaRealElementus/ST1-ASS3/pull/2)
