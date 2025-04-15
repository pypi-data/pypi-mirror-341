from buckaroo.jlisp.lisp_utils import s
from buckaroo.jlisp.lispy import make_interpreter

class JLispRuleParser:
    def __init__(self):
        self.jl_eval, self.sc_eval = make_interpreter()
        self._setup_functions()

    def _setup_functions(self):
        """Setup all the necessary jlisp functions for rule parsing"""
        # Define the core rule evaluation functions
        self.jl_eval([s("define"), s("evaluate-rule"), [s("lambda"), [s("rule"), s("data")],
            [s("let"), [
                [s("rule-type"), [s("car"), s("rule")]],
                [s("comparison"), [s("car"), [s("cdr"), s("rule")]]],
                [s("threshold"), [s("car"), [s("cdr"), [s("cdr"), s("rule")]]]]
            ],
            [s("if"), [s("eq?"), s("rule-type"), s("greatest")],
                [s("evaluate-greatest"), s("rule"), s("data")],
                [s("evaluate-only"), s("rule"), s("data")]]]]])

        self.jl_eval([s("define"), s("evaluate-greatest"), [s("lambda"), [s("rule"), s("data")],
            [s("let"), [
                [s("value"), [s("dict-get"), s("data"), [s("car"), s("rule")], 0.0]],
                [s("threshold"), [s("car"), [s("cdr"), [s("cdr"), s("rule")]]]]
            ],
            [s(">"), s("value"), s("threshold")]]]])

        self.jl_eval([s("define"), s("evaluate-only"), [s("lambda"), [s("rule"), s("data")],
            [s("let"), [
                [s("value"), [s("dict-get"), s("data"), [s("car"), s("rule")], 0.0]],
                [s("threshold"), [s("car"), [s("cdr"), s("rule")]]]
            ],
            [s(">"), s("value"), s("threshold")]]]])

        self.jl_eval([s("define"), s("validate-only-rules"), [s("lambda"), [s("rules")],
            [s("let"), [[s("only-rules"), [s("dict")]]],
                [s("for-each"), [s("lambda"), [s("key"), s("rule")],
                    [s("if"), [s("eq?"), [s("car"), s("rule")], s("only")],
                        [s("let"), [[s("threshold"), [s("car"), [s("cdr"), s("rule")]]]],
                            [s("if"), [s("dict-has-key?"), s("only-rules"), s("threshold")],
                                [s("error"), [s("string-append"),
                                    s("Ambiguous 'only' rules: "), s("key"), s(" and "),
                                    [s("dict-get"), s("only-rules"), s("threshold")],
                                    s(" have the same threshold ("),
                                    [s("number->string"), s("threshold")],
                                    s("). Only rules must have distinct thresholds.")]],
                                [s("dict-set!"), s("only-rules"), s("threshold"), s("key")]]]]],
                s("rules")]]])

        self.jl_eval([s("define"), s("parse-rules"), [s("lambda"), [s("rules")],
            [s("begin"),
                [s("validate-only-rules"), s("rules")],
                s("rules")]]])

        self.jl_eval([s("define"), s("evaluate-rules"), [s("lambda"), [s("rules"), s("data")],
            [s("let"), [
                [s("results"), [s("dict")]],
                [s("greatest-candidates"), [s("list")]],
                [s("only-candidates"), [s("list")]]
            ],
            [s("begin"),
                [s("for-each"), [s("lambda"), [s("key"), s("rule")],
                    [s("let"), [[s("value"), [s("dict-get"), s("data"), s("key"), 0.0]]],
                        [s("dict-set!"), s("results"), s("key"),
                            [s("evaluate-rule"), s("rule"), s("data")]]]],
                    s("rules")],
                
                [s("for-each"), [s("lambda"), [s("key"), s("rule")],
                    [s("if"), [s("dict-get"), s("results"), s("key")],
                        [s("if"), [s("eq?"), [s("car"), s("rule")], s("greatest")],
                            [s("let"), [
                                [s("current-value"), [s("dict-get"), s("data"), s("key"), 0.0]],
                                [s("is-greatest"), s("#t")]
                            ],
                            [s("for-each"), [s("lambda"), [s("other-key")],
                                [s("if"), [s("not"), [s("eq?"), s("other-key"), s("key")]],
                                    [s("set!"), s("is-greatest"),
                                        [s("and"), s("is-greatest"),
                                            [s(">="), s("current-value"),
                                                [s("dict-get"), s("data"), s("other-key"), 0.0]]]]]],
                                [s("dict-keys"), s("rules")]],
                            [s("if"), s("is-greatest"),
                                [s("set!"), s("greatest-candidates"),
                                    [s("cons"), [s("list"), s("key"), s("current-value")],
                                        s("greatest-candidates")]]]],
                            [s("set!"), s("only-candidates"),
                                [s("cons"), [s("list"), s("key"),
                                    [s("dict-get"), s("data"), s("key"), 0.0]],
                                    s("only-candidates")]]]]],
                    s("rules")],
                
                [s("cond"),
                    [[s("not"), [s("null?"), s("only-candidates")]],
                        [s("car"), [s("car"), [s("sort"), s("only-candidates"),
                            [s("lambda"), [s("a"), s("b")],
                                [s(">"), [s("cadr"), s("a")], [s("cadr"), s("b")]]]]]]],
                    [[s("not"), [s("null?"), s("greatest-candidates")]],
                        [s("car"), [s("car"), [s("sort"), s("greatest-candidates"),
                            [s("lambda"), [s("a"), s("b")],
                                [s(">"), [s("cadr"), s("a")], [s("cadr"), s("b")]]]]]]],
                    [s("#t"), s("")]]]]]])

    def parse_rules(self, rules):
        """
        Parse rules in list-based format
        """
        return self.jl_eval([s("parse-rules"), rules])

    def evaluate_rules(self, rules, data):
        """
        Evaluate rules against data
        """
        return self.jl_eval([s("evaluate-rules"), rules, data]) 