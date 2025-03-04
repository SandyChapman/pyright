import collections  # Needed by aliases like DefaultDict, see mypy issue 2986
import sys
from _typeshed import Self, SupportsKeysAndGetItem
from abc import ABCMeta, abstractmethod
from types import BuiltinFunctionType, CodeType, FrameType, FunctionType, MethodType, ModuleType, TracebackType
from typing_extensions import Literal as _Literal, ParamSpec as _ParamSpec, final as _final

if sys.version_info >= (3, 7):
    from types import MethodDescriptorType, MethodWrapperType, WrapperDescriptorType

if sys.version_info >= (3, 9):
    from types import GenericAlias

Any = object()

class TypeVar:
    __name__: str
    __bound__: Type[Any] | None
    __constraints__: Tuple[Type[Any], ...]
    __covariant__: bool
    __contravariant__: bool
    def __init__(
        self,
        name: str,
        *constraints: Type[Any],
        bound: None | Type[Any] | str = ...,
        covariant: bool = ...,
        contravariant: bool = ...,
    ) -> None: ...
    if sys.version_info >= (3, 10):
        def __or__(self, other: Any) -> _SpecialForm: ...
        def __ror__(self, other: Any) -> _SpecialForm: ...

# Used for an undocumented mypy feature. Does not exist at runtime.
_promote = object()

class _SpecialForm:
    def __getitem__(self, typeargs: Any) -> object: ...
    if sys.version_info >= (3, 10):
        def __or__(self, other: Any) -> _SpecialForm: ...
        def __ror__(self, other: Any) -> _SpecialForm: ...

_F = TypeVar("_F", bound=Callable[..., Any])
_P = _ParamSpec("_P")
_T = TypeVar("_T")

def overload(func: _F) -> _F: ...

Union: _SpecialForm = ...
Optional: _SpecialForm = ...
Tuple: _SpecialForm = ...
Generic: _SpecialForm = ...
# Protocol is only present in 3.8 and later, but mypy needs it unconditionally
Protocol: _SpecialForm = ...
Callable: _SpecialForm = ...
Type: _SpecialForm = ...
ClassVar: _SpecialForm = ...
NoReturn: _SpecialForm = ...
if sys.version_info >= (3, 8):
    Final: _SpecialForm = ...
    def final(f: _T) -> _T: ...
    Literal: _SpecialForm = ...
    # TypedDict is a (non-subscriptable) special form.
    TypedDict: object

if sys.version_info < (3, 7):
    class GenericMeta(type): ...

if sys.version_info >= (3, 10):
    class ParamSpecArgs:
        __origin__: ParamSpec
        def __init__(self, origin: ParamSpec) -> None: ...
    class ParamSpecKwargs:
        __origin__: ParamSpec
        def __init__(self, origin: ParamSpec) -> None: ...
    class ParamSpec:
        __name__: str
        __bound__: Type[Any] | None
        __covariant__: bool
        __contravariant__: bool
        def __init__(
            self, name: str, *, bound: None | Type[Any] | str = ..., contravariant: bool = ..., covariant: bool = ...
        ) -> None: ...
        @property
        def args(self) -> ParamSpecArgs: ...
        @property
        def kwargs(self) -> ParamSpecKwargs: ...
        def __or__(self, other: Any) -> _SpecialForm: ...
        def __ror__(self, other: Any) -> _SpecialForm: ...
    Concatenate: _SpecialForm = ...
    TypeAlias: _SpecialForm = ...
    TypeGuard: _SpecialForm = ...
    class NewType:
        def __init__(self, name: str, tp: type) -> None: ...
        def __call__(self, x: _T) -> _T: ...
        def __or__(self, other: Any) -> _SpecialForm: ...
        def __ror__(self, other: Any) -> _SpecialForm: ...
        __supertype__: type

else:
    def NewType(name: str, tp: Type[_T]) -> Type[_T]: ...

# These type variables are used by the container types.
_S = TypeVar("_S")
_KT = TypeVar("_KT")  # Key type.
_VT = TypeVar("_VT")  # Value type.
_T_co = TypeVar("_T_co", covariant=True)  # Any type covariant containers.
_V_co = TypeVar("_V_co", covariant=True)  # Any type covariant containers.
_KT_co = TypeVar("_KT_co", covariant=True)  # Key type covariant containers.
_VT_co = TypeVar("_VT_co", covariant=True)  # Value type covariant containers.
_T_contra = TypeVar("_T_contra", contravariant=True)  # Ditto contravariant.
_TC = TypeVar("_TC", bound=Type[object])

def no_type_check(arg: _F) -> _F: ...
def no_type_check_decorator(decorator: Callable[_P, _T]) -> Callable[_P, _T]: ...  # type: ignore[misc]

# Type aliases and type constructors

class _Alias:
    # Class for defining generic aliases for library types.
    def __getitem__(self, typeargs: Any) -> Any: ...

List = _Alias()
Dict = _Alias()
DefaultDict = _Alias()
Set = _Alias()
FrozenSet = _Alias()
Counter = _Alias()
Deque = _Alias()
ChainMap = _Alias()

if sys.version_info >= (3, 7):
    OrderedDict = _Alias()

if sys.version_info >= (3, 9):
    Annotated: _SpecialForm = ...

# Predefined type variables.
AnyStr = TypeVar("AnyStr", str, bytes)  # noqa: Y001

if sys.version_info >= (3, 8):
    # This class did actually exist in 3.7, but had a different base.
    # We'll just pretend it didn't exist though: the main external use case for _ProtocolMeta is
    # to inherit from for your own custom protocol metaclasses. If you're using 3.7, at runtime
    # you'd use typing_extensions.Protocol, which would be unrelated to typing._ProtocolMeta and
    # so you'd run into metaclass conflicts at runtime if you used typing._ProtocolMeta.
    class _ProtocolMeta(ABCMeta): ...

# Abstract base classes.

def runtime_checkable(cls: _TC) -> _TC: ...
@runtime_checkable
class SupportsInt(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __int__(self) -> int: ...

@runtime_checkable
class SupportsFloat(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __float__(self) -> float: ...

@runtime_checkable
class SupportsComplex(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __complex__(self) -> complex: ...

@runtime_checkable
class SupportsBytes(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __bytes__(self) -> bytes: ...

if sys.version_info >= (3, 8):
    @runtime_checkable
    class SupportsIndex(Protocol, metaclass=ABCMeta):
        @abstractmethod
        def __index__(self) -> int: ...

@runtime_checkable
class SupportsAbs(Protocol[_T_co]):
    @abstractmethod
    def __abs__(self) -> _T_co: ...

@runtime_checkable
class SupportsRound(Protocol[_T_co]):
    @overload
    @abstractmethod
    def __round__(self) -> int: ...
    @overload
    @abstractmethod
    def __round__(self, __ndigits: int) -> _T_co: ...

@runtime_checkable
class Sized(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __len__(self) -> int: ...

@runtime_checkable
class Hashable(Protocol, metaclass=ABCMeta):
    # TODO: This is special, in that a subclass of a hashable class may not be hashable
    #   (for example, list vs. object). It's not obvious how to represent this. This class
    #   is currently mostly useless for static checking.
    @abstractmethod
    def __hash__(self) -> int: ...

@runtime_checkable
class Iterable(Protocol[_T_co]):
    @abstractmethod
    def __iter__(self) -> Iterator[_T_co]: ...

@runtime_checkable
class Iterator(Iterable[_T_co], Protocol[_T_co]):
    @abstractmethod
    def __next__(self) -> _T_co: ...
    def __iter__(self) -> Iterator[_T_co]: ...

@runtime_checkable
class Reversible(Iterable[_T_co], Protocol[_T_co]):
    @abstractmethod
    def __reversed__(self) -> Iterator[_T_co]: ...

class Generator(Iterator[_T_co], Generic[_T_co, _T_contra, _V_co]):
    def __next__(self) -> _T_co: ...
    @abstractmethod
    def send(self, __value: _T_contra) -> _T_co: ...
    @overload
    @abstractmethod
    def throw(
        self, __typ: Type[BaseException], __val: BaseException | object = ..., __tb: TracebackType | None = ...
    ) -> _T_co: ...
    @overload
    @abstractmethod
    def throw(self, __typ: BaseException, __val: None = ..., __tb: TracebackType | None = ...) -> _T_co: ...
    def close(self) -> None: ...
    def __iter__(self) -> Generator[_T_co, _T_contra, _V_co]: ...
    @property
    def gi_code(self) -> CodeType: ...
    @property
    def gi_frame(self) -> FrameType: ...
    @property
    def gi_running(self) -> bool: ...
    @property
    def gi_yieldfrom(self) -> Generator[Any, Any, Any] | None: ...

@runtime_checkable
class Awaitable(Protocol[_T_co]):
    @abstractmethod
    def __await__(self) -> Generator[Any, None, _T_co]: ...

class Coroutine(Awaitable[_V_co], Generic[_T_co, _T_contra, _V_co]):
    __name__: str
    __qualname__: str
    @property
    def cr_await(self) -> Any | None: ...
    @property
    def cr_code(self) -> CodeType: ...
    @property
    def cr_frame(self) -> FrameType: ...
    @property
    def cr_running(self) -> bool: ...
    @abstractmethod
    def send(self, __value: _T_contra) -> _T_co: ...
    @overload
    @abstractmethod
    def throw(
        self, __typ: Type[BaseException], __val: BaseException | object = ..., __tb: TracebackType | None = ...
    ) -> _T_co: ...
    @overload
    @abstractmethod
    def throw(self, __typ: BaseException, __val: None = ..., __tb: TracebackType | None = ...) -> _T_co: ...
    @abstractmethod
    def close(self) -> None: ...

# NOTE: This type does not exist in typing.py or PEP 484 but mypy needs it to exist.
# The parameters correspond to Generator, but the 4th is the original type.
class AwaitableGenerator(
    Awaitable[_V_co], Generator[_T_co, _T_contra, _V_co], Generic[_T_co, _T_contra, _V_co, _S], metaclass=ABCMeta
): ...

@runtime_checkable
class AsyncIterable(Protocol[_T_co]):
    @abstractmethod
    def __aiter__(self) -> AsyncIterator[_T_co]: ...

@runtime_checkable
class AsyncIterator(AsyncIterable[_T_co], Protocol[_T_co]):
    @abstractmethod
    def __anext__(self) -> Awaitable[_T_co]: ...
    def __aiter__(self) -> AsyncIterator[_T_co]: ...

class AsyncGenerator(AsyncIterator[_T_co], Generic[_T_co, _T_contra]):
    @abstractmethod
    def __anext__(self) -> Awaitable[_T_co]: ...
    @abstractmethod
    def asend(self, __value: _T_contra) -> Awaitable[_T_co]: ...
    @overload
    @abstractmethod
    def athrow(
        self, __typ: Type[BaseException], __val: BaseException | object = ..., __tb: TracebackType | None = ...
    ) -> Awaitable[_T_co]: ...
    @overload
    @abstractmethod
    def athrow(self, __typ: BaseException, __val: None = ..., __tb: TracebackType | None = ...) -> Awaitable[_T_co]: ...
    @abstractmethod
    def aclose(self) -> Awaitable[None]: ...
    @abstractmethod
    def __aiter__(self) -> AsyncGenerator[_T_co, _T_contra]: ...
    @property
    def ag_await(self) -> Any: ...
    @property
    def ag_code(self) -> CodeType: ...
    @property
    def ag_frame(self) -> FrameType: ...
    @property
    def ag_running(self) -> bool: ...

@runtime_checkable
class Container(Protocol[_T_co]):
    @abstractmethod
    def __contains__(self, __x: object) -> bool: ...

@runtime_checkable
class Collection(Iterable[_T_co], Container[_T_co], Protocol[_T_co]):
    # Implement Sized (but don't have it as a base class).
    @abstractmethod
    def __len__(self) -> int: ...

class Sequence(Collection[_T_co], Reversible[_T_co], Generic[_T_co]):
    @overload
    @abstractmethod
    def __getitem__(self, i: int) -> _T_co: ...
    @overload
    @abstractmethod
    def __getitem__(self, s: slice) -> Sequence[_T_co]: ...
    # Mixin methods
    def index(self, value: Any, start: int = ..., stop: int = ...) -> int: ...
    def count(self, value: Any) -> int: ...
    def __contains__(self, x: object) -> bool: ...
    def __iter__(self) -> Iterator[_T_co]: ...
    def __reversed__(self) -> Iterator[_T_co]: ...

class MutableSequence(Sequence[_T], Generic[_T]):
    @abstractmethod
    def insert(self, index: int, value: _T) -> None: ...
    @overload
    @abstractmethod
    def __getitem__(self, i: int) -> _T: ...
    @overload
    @abstractmethod
    def __getitem__(self, s: slice) -> MutableSequence[_T]: ...
    @overload
    @abstractmethod
    def __setitem__(self, i: int, o: _T) -> None: ...
    @overload
    @abstractmethod
    def __setitem__(self, s: slice, o: Iterable[_T]) -> None: ...
    @overload
    @abstractmethod
    def __delitem__(self, i: int) -> None: ...
    @overload
    @abstractmethod
    def __delitem__(self, i: slice) -> None: ...
    # Mixin methods
    def append(self, value: _T) -> None: ...
    def clear(self) -> None: ...
    def extend(self, values: Iterable[_T]) -> None: ...
    def reverse(self) -> None: ...
    def pop(self, index: int = ...) -> _T: ...
    def remove(self, value: _T) -> None: ...
    def __iadd__(self, x: Iterable[_T]) -> MutableSequence[_T]: ...

class AbstractSet(Collection[_T_co], Generic[_T_co]):
    @abstractmethod
    def __contains__(self, x: object) -> bool: ...
    # Mixin methods
    def __le__(self, s: AbstractSet[Any]) -> bool: ...
    def __lt__(self, s: AbstractSet[Any]) -> bool: ...
    def __gt__(self, s: AbstractSet[Any]) -> bool: ...
    def __ge__(self, s: AbstractSet[Any]) -> bool: ...
    def __and__(self, s: AbstractSet[Any]) -> AbstractSet[_T_co]: ...
    def __or__(self, s: AbstractSet[_T]) -> AbstractSet[_T_co | _T]: ...
    def __sub__(self, s: AbstractSet[Any]) -> AbstractSet[_T_co]: ...
    def __xor__(self, s: AbstractSet[_T]) -> AbstractSet[_T_co | _T]: ...
    def isdisjoint(self, other: Iterable[Any]) -> bool: ...

class MutableSet(AbstractSet[_T], Generic[_T]):
    @abstractmethod
    def add(self, value: _T) -> None: ...
    @abstractmethod
    def discard(self, value: _T) -> None: ...
    # Mixin methods
    def clear(self) -> None: ...
    def pop(self) -> _T: ...
    def remove(self, value: _T) -> None: ...
    def __ior__(self, s: AbstractSet[_S]) -> MutableSet[_T | _S]: ...
    def __iand__(self, s: AbstractSet[Any]) -> MutableSet[_T]: ...
    def __ixor__(self, s: AbstractSet[_S]) -> MutableSet[_T | _S]: ...
    def __isub__(self, s: AbstractSet[Any]) -> MutableSet[_T]: ...

class MappingView(Sized):
    def __init__(self, mapping: Mapping[Any, Any]) -> None: ...  # undocumented
    def __len__(self) -> int: ...

class ItemsView(MappingView, AbstractSet[Tuple[_KT_co, _VT_co]], Generic[_KT_co, _VT_co]):
    def __init__(self, mapping: Mapping[_KT_co, _VT_co]) -> None: ...  # undocumented
    def __and__(self, o: Iterable[Any]) -> set[tuple[_KT_co, _VT_co]]: ...
    def __rand__(self, o: Iterable[_T]) -> set[_T]: ...
    def __contains__(self, o: object) -> bool: ...
    def __iter__(self) -> Iterator[tuple[_KT_co, _VT_co]]: ...
    if sys.version_info >= (3, 8):
        def __reversed__(self) -> Iterator[tuple[_KT_co, _VT_co]]: ...
    def __or__(self, o: Iterable[_T]) -> set[tuple[_KT_co, _VT_co] | _T]: ...
    def __ror__(self, o: Iterable[_T]) -> set[tuple[_KT_co, _VT_co] | _T]: ...
    def __sub__(self, o: Iterable[Any]) -> set[tuple[_KT_co, _VT_co]]: ...
    def __rsub__(self, o: Iterable[_T]) -> set[_T]: ...
    def __xor__(self, o: Iterable[_T]) -> set[tuple[_KT_co, _VT_co] | _T]: ...
    def __rxor__(self, o: Iterable[_T]) -> set[tuple[_KT_co, _VT_co] | _T]: ...

class KeysView(MappingView, AbstractSet[_KT_co], Generic[_KT_co]):
    def __init__(self, mapping: Mapping[_KT_co, Any]) -> None: ...  # undocumented
    def __and__(self, o: Iterable[Any]) -> set[_KT_co]: ...
    def __rand__(self, o: Iterable[_T]) -> set[_T]: ...
    def __contains__(self, o: object) -> bool: ...
    def __iter__(self) -> Iterator[_KT_co]: ...
    if sys.version_info >= (3, 8):
        def __reversed__(self) -> Iterator[_KT_co]: ...
    def __or__(self, o: Iterable[_T]) -> set[_KT_co | _T]: ...
    def __ror__(self, o: Iterable[_T]) -> set[_KT_co | _T]: ...
    def __sub__(self, o: Iterable[Any]) -> set[_KT_co]: ...
    def __rsub__(self, o: Iterable[_T]) -> set[_T]: ...
    def __xor__(self, o: Iterable[_T]) -> set[_KT_co | _T]: ...
    def __rxor__(self, o: Iterable[_T]) -> set[_KT_co | _T]: ...

class ValuesView(MappingView, Iterable[_VT_co], Generic[_VT_co]):
    def __init__(self, mapping: Mapping[Any, _VT_co]) -> None: ...  # undocumented
    def __contains__(self, o: object) -> bool: ...
    def __iter__(self) -> Iterator[_VT_co]: ...
    if sys.version_info >= (3, 8):
        def __reversed__(self) -> Iterator[_VT_co]: ...

@runtime_checkable
class ContextManager(Protocol[_T_co]):
    def __enter__(self) -> _T_co: ...
    def __exit__(
        self, __exc_type: Type[BaseException] | None, __exc_value: BaseException | None, __traceback: TracebackType | None
    ) -> bool | None: ...

@runtime_checkable
class AsyncContextManager(Protocol[_T_co]):
    def __aenter__(self) -> Awaitable[_T_co]: ...
    def __aexit__(
        self, __exc_type: Type[BaseException] | None, __exc_value: BaseException | None, __traceback: TracebackType | None
    ) -> Awaitable[bool | None]: ...

class Mapping(Collection[_KT], Generic[_KT, _VT_co]):
    # TODO: We wish the key type could also be covariant, but that doesn't work,
    # see discussion in https://github.com/python/typing/pull/273.
    @abstractmethod
    def __getitem__(self, __k: _KT) -> _VT_co: ...
    # Mixin methods
    @overload
    def get(self, key: _KT) -> _VT_co | None: ...
    @overload
    def get(self, __key: _KT, __default: _VT_co | _T) -> _VT_co | _T: ...
    def items(self) -> ItemsView[_KT, _VT_co]: ...
    def keys(self) -> KeysView[_KT]: ...
    def values(self) -> ValuesView[_VT_co]: ...
    def __contains__(self, __o: object) -> bool: ...

class MutableMapping(Mapping[_KT, _VT], Generic[_KT, _VT]):
    @abstractmethod
    def __setitem__(self, __k: _KT, __v: _VT) -> None: ...
    @abstractmethod
    def __delitem__(self, __v: _KT) -> None: ...
    def clear(self) -> None: ...
    @overload
    def pop(self, __key: _KT) -> _VT: ...
    @overload
    def pop(self, __key: _KT, __default: _VT | _T = ...) -> _VT | _T: ...
    def popitem(self) -> tuple[_KT, _VT]: ...
    def setdefault(self, __key: _KT, __default: _VT = ...) -> _VT: ...
    # 'update' used to take a Union, but using overloading is better.
    # The second overloaded type here is a bit too general, because
    # Mapping[Tuple[_KT, _VT], W] is a subclass of Iterable[Tuple[_KT, _VT]],
    # but will always have the behavior of the first overloaded type
    # at runtime, leading to keys of a mix of types _KT and Tuple[_KT, _VT].
    # We don't currently have any way of forcing all Mappings to use
    # the first overload, but by using overloading rather than a Union,
    # mypy will commit to using the first overload when the argument is
    # known to be a Mapping with unknown type parameters, which is closer
    # to the behavior we want. See mypy issue  #1430.
    @overload
    def update(self, __m: SupportsKeysAndGetItem[_KT, _VT], **kwargs: _VT) -> None: ...
    @overload
    def update(self, __m: Iterable[tuple[_KT, _VT]], **kwargs: _VT) -> None: ...
    @overload
    def update(self, **kwargs: _VT) -> None: ...

Text = str

TYPE_CHECKING = True

# In stubs, the arguments of the IO class are marked as positional-only.
# This differs from runtime, but better reflects the fact that in reality
# classes deriving from IO use different names for the arguments.
class IO(Iterator[AnyStr], Generic[AnyStr]):
    # TODO use abstract properties
    @property
    def mode(self) -> str: ...
    @property
    def name(self) -> str: ...
    @abstractmethod
    def close(self) -> None: ...
    @property
    def closed(self) -> bool: ...
    @abstractmethod
    def fileno(self) -> int: ...
    @abstractmethod
    def flush(self) -> None: ...
    @abstractmethod
    def isatty(self) -> bool: ...
    @abstractmethod
    def read(self, __n: int = ...) -> AnyStr: ...
    @abstractmethod
    def readable(self) -> bool: ...
    @abstractmethod
    def readline(self, __limit: int = ...) -> AnyStr: ...
    @abstractmethod
    def readlines(self, __hint: int = ...) -> list[AnyStr]: ...
    @abstractmethod
    def seek(self, __offset: int, __whence: int = ...) -> int: ...
    @abstractmethod
    def seekable(self) -> bool: ...
    @abstractmethod
    def tell(self) -> int: ...
    @abstractmethod
    def truncate(self, __size: int | None = ...) -> int: ...
    @abstractmethod
    def writable(self) -> bool: ...
    @abstractmethod
    def write(self, __s: AnyStr) -> int: ...
    @abstractmethod
    def writelines(self, __lines: Iterable[AnyStr]) -> None: ...
    @abstractmethod
    def __next__(self) -> AnyStr: ...
    @abstractmethod
    def __iter__(self) -> Iterator[AnyStr]: ...
    @abstractmethod
    def __enter__(self) -> IO[AnyStr]: ...
    @abstractmethod
    def __exit__(
        self, __t: Type[BaseException] | None, __value: BaseException | None, __traceback: TracebackType | None
    ) -> bool | None: ...

class BinaryIO(IO[bytes]):
    @abstractmethod
    def __enter__(self) -> BinaryIO: ...

class TextIO(IO[str]):
    # TODO use abstractproperty
    @property
    def buffer(self) -> BinaryIO: ...
    @property
    def encoding(self) -> str: ...
    @property
    def errors(self) -> str | None: ...
    @property
    def line_buffering(self) -> int: ...  # int on PyPy, bool on CPython
    @property
    def newlines(self) -> Any: ...  # None, str or tuple
    @abstractmethod
    def __enter__(self) -> TextIO: ...

class ByteString(Sequence[int], metaclass=ABCMeta): ...

@_final
class Match(Generic[AnyStr]):
    pos: int
    endpos: int
    lastindex: int | None
    lastgroup: str | None
    string: AnyStr

    # The regular expression object whose match() or search() method produced
    # this match instance.
    re: Pattern[AnyStr]
    def expand(self, template: AnyStr) -> AnyStr: ...
    # group() returns "AnyStr" or "AnyStr | None", depending on the pattern.
    @overload
    def group(self, __group: _Literal[0] = ...) -> AnyStr: ...
    @overload
    def group(self, __group: str | int) -> AnyStr | Any: ...
    @overload
    def group(self, __group1: str | int, __group2: str | int, *groups: str | int) -> Tuple[AnyStr | Any, ...]: ...
    # Each item of groups()'s return tuple is either "AnyStr" or
    # "AnyStr | None", depending on the pattern.
    @overload
    def groups(self) -> Tuple[AnyStr | Any, ...]: ...
    @overload
    def groups(self, default: _T) -> Tuple[AnyStr | _T, ...]: ...
    # Each value in groupdict()'s return dict is either "AnyStr" or
    # "AnyStr | None", depending on the pattern.
    @overload
    def groupdict(self) -> dict[str, AnyStr | Any]: ...
    @overload
    def groupdict(self, default: _T) -> dict[str, AnyStr | _T]: ...
    def start(self, __group: int | str = ...) -> int: ...
    def end(self, __group: int | str = ...) -> int: ...
    def span(self, __group: int | str = ...) -> tuple[int, int]: ...
    @property
    def regs(self) -> Tuple[tuple[int, int], ...]: ...  # undocumented
    # __getitem__() returns "AnyStr" or "AnyStr | None", depending on the pattern.
    @overload
    def __getitem__(self, __key: _Literal[0]) -> AnyStr: ...
    @overload
    def __getitem__(self, __key: int | str) -> AnyStr | Any: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...

@_final
class Pattern(Generic[AnyStr]):
    flags: int
    groupindex: Mapping[str, int]
    groups: int
    pattern: AnyStr
    def search(self, string: AnyStr, pos: int = ..., endpos: int = ...) -> Match[AnyStr] | None: ...
    def match(self, string: AnyStr, pos: int = ..., endpos: int = ...) -> Match[AnyStr] | None: ...
    def fullmatch(self, string: AnyStr, pos: int = ..., endpos: int = ...) -> Match[AnyStr] | None: ...
    def split(self, string: AnyStr, maxsplit: int = ...) -> list[AnyStr | Any]: ...
    def findall(self, string: AnyStr, pos: int = ..., endpos: int = ...) -> list[Any]: ...
    def finditer(self, string: AnyStr, pos: int = ..., endpos: int = ...) -> Iterator[Match[AnyStr]]: ...
    @overload
    def sub(self, repl: AnyStr, string: AnyStr, count: int = ...) -> AnyStr: ...
    @overload
    def sub(self, repl: Callable[[Match[AnyStr]], AnyStr], string: AnyStr, count: int = ...) -> AnyStr: ...
    @overload
    def subn(self, repl: AnyStr, string: AnyStr, count: int = ...) -> tuple[AnyStr, int]: ...
    @overload
    def subn(self, repl: Callable[[Match[AnyStr]], AnyStr], string: AnyStr, count: int = ...) -> tuple[AnyStr, int]: ...
    if sys.version_info >= (3, 9):
        def __class_getitem__(cls, item: Any) -> GenericAlias: ...

# Functions

if sys.version_info >= (3, 7):
    _get_type_hints_obj_allowed_types = Union[
        object,
        Callable[..., Any],
        FunctionType,
        BuiltinFunctionType,
        MethodType,
        ModuleType,
        WrapperDescriptorType,
        MethodWrapperType,
        MethodDescriptorType,
    ]
else:
    _get_type_hints_obj_allowed_types = Union[
        object, Callable[..., Any], FunctionType, BuiltinFunctionType, MethodType, ModuleType,
    ]

if sys.version_info >= (3, 9):
    def get_type_hints(
        obj: _get_type_hints_obj_allowed_types,
        globalns: dict[str, Any] | None = ...,
        localns: dict[str, Any] | None = ...,
        include_extras: bool = ...,
    ) -> dict[str, Any]: ...

else:
    def get_type_hints(
        obj: _get_type_hints_obj_allowed_types, globalns: dict[str, Any] | None = ..., localns: dict[str, Any] | None = ...
    ) -> dict[str, Any]: ...

if sys.version_info >= (3, 8):
    def get_origin(tp: Any) -> Any | None: ...
    def get_args(tp: Any) -> Tuple[Any, ...]: ...

@overload
def cast(typ: Type[_T], val: Any) -> _T: ...
@overload
def cast(typ: str, val: Any) -> Any: ...
@overload
def cast(typ: object, val: Any) -> Any: ...

# Type constructors

class NamedTuple(Tuple[Any, ...]):
    if sys.version_info < (3, 8):
        _field_types: collections.OrderedDict[str, type]
    elif sys.version_info < (3, 9):
        _field_types: dict[str, type]
    _field_defaults: dict[str, Any]
    _fields: Tuple[str, ...]
    _source: str
    @overload
    def __init__(self, typename: str, fields: Iterable[tuple[str, Any]] = ...) -> None: ...
    @overload
    def __init__(self, typename: str, fields: None = ..., **kwargs: Any) -> None: ...
    @classmethod
    def _make(cls: Type[_T], iterable: Iterable[Any]) -> _T: ...
    if sys.version_info >= (3, 8):
        def _asdict(self) -> dict[str, Any]: ...
    else:
        def _asdict(self) -> collections.OrderedDict[str, Any]: ...
    def _replace(self: Self, **kwargs: Any) -> Self: ...

# Internal mypy fallback type for all typed dicts (does not exist at runtime)
class _TypedDict(Mapping[str, object], metaclass=ABCMeta):
    def copy(self: Self) -> Self: ...
    # Using NoReturn so that only calls using mypy plugin hook that specialize the signature
    # can go through.
    def setdefault(self, k: NoReturn, default: object) -> object: ...
    # Mypy plugin hook for 'pop' expects that 'default' has a type variable type.
    def pop(self, k: NoReturn, default: _T = ...) -> object: ...  # type: ignore
    def update(self: _T, __m: _T) -> None: ...
    def __delitem__(self, k: NoReturn) -> None: ...
    def items(self) -> ItemsView[str, object]: ...
    def keys(self) -> KeysView[str]: ...
    def values(self) -> ValuesView[object]: ...
    def __or__(self: Self, __value: Self) -> Self: ...
    def __ior__(self: Self, __value: Self) -> Self: ...

# This itself is only available during type checking
def type_check_only(func_or_cls: _F) -> _F: ...

if sys.version_info >= (3, 7):
    class ForwardRef:
        __forward_arg__: str
        __forward_code__: CodeType
        __forward_evaluated__: bool
        __forward_value__: Any | None
        __forward_is_argument__: bool
        if sys.version_info >= (3, 9):
            # The module and is_class arguments were added in later Python 3.9 versions.
            def __init__(self, arg: str, is_argument: bool = ..., module: Any | None = ..., *, is_class: bool = ...) -> None: ...
        else:
            def __init__(self, arg: str, is_argument: bool = ...) -> None: ...
        def _evaluate(self, globalns: dict[str, Any] | None, localns: dict[str, Any] | None) -> Any | None: ...
        def __eq__(self, other: Any) -> bool: ...
        def __hash__(self) -> int: ...
        if sys.version_info >= (3, 11):
            def __or__(self, other: Any) -> _SpecialForm: ...
            def __ror__(self, other: Any) -> _SpecialForm: ...

if sys.version_info >= (3, 10):
    def is_typeddict(tp: object) -> bool: ...
