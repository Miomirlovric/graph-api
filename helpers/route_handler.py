from typing import Any, Callable, Iterable

from helpers.validators import ValidationChain, Validator


def execute_analysis(
    req,
    *,
    pre_build_validators: Iterable[Validator] = (),
    graph_builder: Callable[[Any], Any],
    post_build_validators: Iterable[Validator] = (),
    compute: Callable[..., Any],
):
    ValidationChain(pre_build_validators).run(req)
    graph = graph_builder(req)
    ValidationChain(post_build_validators).run(graph)
    return compute(graph, req)
