# symbol_data.py
"""
모든 심볼 카테고리 데이터 정의
"""


class SymbolData:
    """심볼 데이터 관리 클래스"""

    @staticmethod
    def get_lowercase_greek():
        return [
            ("α", r"\alpha", "alpha"),
            ("β", r"\beta", "beta"),
            ("γ", r"\gamma", "gamma"),
            ("δ", r"\delta", "delta"),
            ("ε", r"\epsilon", "epsilon"),
            ("ϵ", r"\varepsilon", "varepsilon"),
            ("ζ", r"\zeta", "zeta"),
            ("η", r"\eta", "eta"),
            ("θ", r"\theta", "theta"),
            ("ϑ", r"\vartheta", "vartheta"),
            ("ι", r"\iota", "iota"),
            ("κ", r"\kappa", "kappa"),
            ("ϰ", r"\varkappa", "varkappa"),
            ("λ", r"\lambda", "lambda"),
            ("μ", r"\mu", "mu"),
            ("ν", r"\nu", "nu"),
            ("ξ", r"\xi", "xi"),
            ("ο", "o", "omicron"),
            ("π", r"\pi", "pi"),
            ("ϖ", r"\varpi", "varpi"),
            ("ρ", r"\rho", "rho"),
            ("ϱ", r"\varrho", "varrho"),
            ("σ", r"\sigma", "sigma"),
            ("ς", r"\varsigma", "varsigma"),
            ("τ", r"\tau", "tau"),
            ("υ", r"\upsilon", "upsilon"),
            ("φ", r"\phi", "phi"),
            ("ϕ", r"\varphi", "varphi"),
            ("χ", r"\chi", "chi"),
            ("ψ", r"\psi", "psi"),
            ("ω", r"\omega", "omega"),
        ]

    @staticmethod
    def get_uppercase_greek():
        return [
            ("Α", "A", "Alpha"),
            ("Β", "B", "Beta"),
            ("Γ", r"\Gamma", "Gamma"),
            ("Δ", r"\Delta", "Delta"),
            ("Ε", "E", "Epsilon"),
            ("Ζ", "Z", "Zeta"),
            ("Η", "H", "Eta"),
            ("Θ", r"\Theta", "Theta"),
            ("Ι", "I", "Iota"),
            ("Κ", "K", "Kappa"),
            ("Λ", r"\Lambda", "Lambda"),
            ("Μ", "M", "Mu"),
            ("Ν", "N", "Nu"),
            ("Ξ", r"\Xi", "Xi"),
            ("Ο", "O", "Omicron"),
            ("Π", r"\Pi", "Pi"),
            ("Ρ", "P", "Rho"),
            ("Σ", r"\Sigma", "Sigma"),
            ("Τ", "T", "Tau"),
            ("Υ", r"\Upsilon", "Upsilon"),
            ("Φ", r"\Phi", "Phi"),
            ("Χ", "X", "Chi"),
            ("Ψ", r"\Psi", "Psi"),
            ("Ω", r"\Omega", "Omega"),
        ]

    @staticmethod
    def get_script_letters():
        return [
            ("𝒜", r"\mathcal{A}", "Script A"),
            ("ℬ", r"\mathcal{B}", "Script B"),
            ("𝒞", r"\mathcal{C}", "Script C"),
            ("𝒟", r"\mathcal{D}", "Script D"),
            ("ℰ", r"\mathcal{E}", "Script E"),
            ("ℱ", r"\mathcal{F}", "Script F"),
            ("𝒢", r"\mathcal{G}", "Script G"),
            ("ℋ", r"\mathcal{H}", "Script H"),
            ("ℐ", r"\mathcal{I}", "Script I"),
            ("𝒥", r"\mathcal{J}", "Script J"),
            ("𝒦", r"\mathcal{K}", "Script K"),
            ("ℒ", r"\mathcal{L}", "Script L"),
            ("ℳ", r"\mathcal{M}", "Script M"),
            ("𝒩", r"\mathcal{N}", "Script N"),
            ("𝒪", r"\mathcal{O}", "Script O"),
            ("𝒫", r"\mathcal{P}", "Script P"),
            ("𝒬", r"\mathcal{Q}", "Script Q"),
            ("ℛ", r"\mathcal{R}", "Script R"),
            ("𝒮", r"\mathcal{S}", "Script S"),
            ("𝒯", r"\mathcal{T}", "Script T"),
            ("𝒰", r"\mathcal{U}", "Script U"),
            ("𝒱", r"\mathcal{V}", "Script V"),
            ("𝒲", r"\mathcal{W}", "Script W"),
            ("𝒳", r"\mathcal{X}", "Script X"),
            ("𝒴", r"\mathcal{Y}", "Script Y"),
            ("𝒵", r"\mathcal{Z}", "Script Z"),
            ("𝒻", r"\mathcal{f}", "Script f"),
            ("𝒽", r"\mathcal{h}", "Script h"),
            ("𝒾", r"\mathcal{i}", "Script i"),
            ("𝓁", r"\mathcal{l}", "Script l"),
            ("𝓂", r"\mathcal{m}", "Script m"),
            ("𝓃", r"\mathcal{n}", "Script n"),
            ("𝓅", r"\mathcal{p}", "Script p"),
            ("𝓇", r"\mathcal{r}", "Script r"),
            ("𝓉", r"\mathcal{t}", "Script t"),
        ]

    @staticmethod
    def get_math_symbols():
        return [
            ("∑", r"\sum_{i=1}^{n}", "Sum"),
            ("∏", r"\prod_{i=1}^{n}", "Product"),
            ("∂", r"\partial", "Partial"),
            ("∇", r"\nabla", "Nabla"),
            ("∞", r"\infty", "Infinity"),
            ("∫", r"\int_{a}^{b}", "Integral"),
            ("≈", r"\approx", "Approximately"),
            ("≠", r"\neq", "Not Equal"),
            ("≤", r"\leq", "Less Than or Equal"),
            ("≥", r"\geq", "Greater Than or Equal"),
            ("∈", r"\in", "Element Of"),
            ("⊂", r"\subset", "Subset"),
            ("∩", r"\cap", "Intersection"),
            ("∪", r"\cup", "Union"),
            ("→", r"\rightarrow", "Right Arrow"),
            ("←", r"\leftarrow", "Left Arrow"),
            ("↔", r"\leftrightarrow", "Double Arrow"),
            ("≡", r"\equiv", "Identical To"),
            ("≅", r"\cong", "Congruent To"),
            ("≜", r"\triangleq", "Defined As"),
        ]

    @staticmethod
    def get_vector_symbols():
        return [
            ("·", r"\cdot", "Dot Product"),
            ("×", r"\times", "Cross Product"),
            ("⊗", r"\otimes", "Tensor Product"),
            ("⊕", r"\oplus", "Direct Sum"),
            ("⟨", r"\langle", "Left Angle Bracket"),
            ("⟩", r"\rangle", "Right Angle Bracket"),
            ("‖", r"\|", "Norm"),
            ("⊥", r"\perp", "Perpendicular"),
            ("∥", r"\parallel", "Parallel"),
            ("†", r"^\dagger", "Conjugate Transpose"),
            ("⊙", r"\odot", "Hadamard Product"),
            ("⨂", r"\bigotimes", "Kronecker Product"),
            ("⨁", r"\bigoplus", "Direct Sum Operator"),
            ("⟦", r"\llbracket", "Left Double Bracket"),
            ("⟧", r"\rrbracket", "Right Double Bracket"),
        ]

    @staticmethod
    def get_set_symbols():
        return [
            ("∅", r"\emptyset", "Empty Set"),
            ("∀", r"\forall", "For All"),
            ("∃", r"\exists", "There Exists"),
            ("∄", r"\nexists", "Does Not Exist"),
            ("∉", r"\notin", "Not Element Of"),
            ("⊄", r"\not\subset", "Not Subset"),
            ("⊆", r"\subseteq", "Subset or Equal"),
            ("⊇", r"\supseteq", "Superset or Equal"),
            ("⊊", r"\subsetneq", "Proper Subset"),
            ("⊋", r"\supsetneq", "Proper Superset"),
            ("ℕ", r"\mathbb{N}", "Natural Numbers"),
            ("ℤ", r"\mathbb{Z}", "Integers"),
            ("ℚ", r"\mathbb{Q}", "Rational Numbers"),
            ("ℝ", r"\mathbb{R}", "Real Numbers"),
            ("ℂ", r"\mathbb{C}", "Complex Numbers"),
            ("ℙ", r"\mathbb{P}", "Prime Numbers"),
            ("△", r"\triangle", "Symmetric Difference"),
            ("×", r"\times", "Cartesian Product"),
        ]

    @staticmethod
    def get_logic_symbols():
        return [
            ("¬", r"\neg", "Negation/Not"),
            ("∧", r"\wedge", "Logical And"),
            ("∨", r"\vee", "Logical Or"),
            ("⊻", r"\veebar", "Exclusive Or"),
            ("⇒", r"\Rightarrow", "Implies"),
            ("⇔", r"\Leftrightarrow", "If and Only If"),
            ("⊨", r"\models", "Models/Entails"),
            ("⊢", r"\vdash", "Proves"),
            ("□", r"\Box", "Necessary"),
            ("◊", r"\Diamond", "Possible"),
            ("⊤", r"\top", "Top/True"),
            ("⊥", r"\bot", "Bottom/False"),
            ("≡", r"\equiv", "Logical Equivalence"),
            ("⊦", r"\vdash", "Assertion"),
        ]

    @staticmethod
    def get_stat_symbols():
        return [
            ("𝔼", r"\mathbb{E}", "Expected Value"),
            ("ℙ", r"\mathbb{P}", "Probability"),
            ("𝕍", r"\mathbb{V}", "Variance"),
            ("√", r"\sqrt{x}", "Square Root"),
            ("∝", r"\propto", "Proportional To"),
            ("±", r"\pm", "Plus-Minus"),
            ("∼", r"\sim", "Distributed As"),
            ("≫", r"\gg", "Much Greater Than"),
            ("≪", r"\ll", "Much Less Than"),
            ("μ̂", r"\hat{\mu}", "mu hat - estimator"),
            ("σ̂", r"\hat{\sigma}", "sigma hat - estimator"),
            ("ρ", r"\rho", "rho - correlation"),
            ("χ²", r"\chi^2", "Chi-Squared"),
            ("σ²", r"\sigma^2", "Variance"),
            ("⟂", r"\perp", "Independent"),
            ("∩", r"\cap", "Intersection/And"),
            ("∪", r"\cup", "Union/Or"),
        ]

    @staticmethod
    def get_physics_symbols():
        return [
            ("ℏ", r"\hbar", "h-bar"),
            ("ψ", r"\psi", "wavefunction"),
            ("Ψ", r"\Psi", "Wavefunction"),
            ("⟨ϕ|ψ⟩", r"\langle \phi | \psi \rangle", "Bracket Notation"),
            ("⊗", r"\otimes", "Tensor Product"),
            ("†", r"^\dagger", "Hermitian Conjugate"),
            ("°", r"^\circ", "Degree"),
            ("∮", r"\oint", "Contour Integral"),
            ("∯", r"\oiint", "Surface Integral"),
            ("∰", r"\oiiint", "Volume Integral"),
            ("∇²", r"\nabla^2", "Laplacian"),
            ("×", r"\times", "Curl Operator"),
            ("γ", r"\gamma", "Lorentz Factor"),
            ("Λ", r"\Lambda", "Lambda/Cosmological Constant"),
            ("⟨Â⟩", r"\langle \hat{A} \rangle", "Expectation Value"),
            ("⨂", r"\bigotimes", "Tensor Product Operator"),
        ]

    @staticmethod
    def get_calculus_symbols():
        return [
            ("∫", r"\int_{a}^{b}", "Definite Integral"),
            ("∫", r"\int", "Indefinite Integral"),
            ("∬", r"\iint_{D}", "Double Integral"),
            ("∭", r"\iiint_{V}", "Triple Integral"),
            ("∮", r"\oint_{C}", "Contour Integral"),
            ("∯", r"\oiint_{S}", "Surface Integral"),
            ("∰", r"\oiiint_{V}", "Volume Integral"),
            ("∂x", r"\frac{\partial}{\partial x}", "Partial wrt x"),
            ("∂y", r"\frac{\partial}{\partial y}", "Partial wrt y"),
            ("∂z", r"\frac{\partial}{\partial z}", "Partial wrt z"),
            ("∂t", r"\frac{\partial}{\partial t}", "Partial wrt t"),
            ("′", r"^\prime", "Prime/Derivative"),
            ("″", r"^{\prime\prime}", "Double Prime"),
            ("dx", "dx", "Differential x"),
            ("∇f", r"\nabla f", "Gradient"),
            ("lim", r"\lim_{x \to a}", "Limit"),
            ("δ", r"\delta", "Variation/Functional Derivative"),
            ("ε", r"\epsilon", "Epsilon/Small Quantity"),
        ]

    @staticmethod
    def get_ai_symbols():
        return [
            ("∇θ", r"\nabla_\theta", "Gradient wrt Parameters"),
            ("∑", r"\sum_{i=1}^{n}", "Summation"),
            ("∏", r"\prod_{i=1}^{n}", "Product"),
            ("𝔼", r"\mathbb{E}", "Expected Value"),
            ("ℙ", r"\mathbb{P}", "Probability"),
            ("𝕍", r"\mathbb{V}", "Variance"),
            ("⊗", r"\otimes", "Tensor Product"),
            ("⊕", r"\oplus", "Direct Sum"),
            ("⊙", r"\odot", "Hadamard Product"),
            ("∥W∥", r"\|W\|", "Norm of Weights"),
            ("θ̂", r"\hat{\theta}", "Parameter Estimate"),
            ("ŷ", r"\hat{y}", "Prediction"),
            ("𝓛", r"\mathcal{L}", "Loss Function"),
            (
                "∂𝓛/∂θ",
                r"\frac{\partial\mathcal{L}}{\partial\theta}",
                "Gradient of Loss",
            ),
            ("≈", r"\approx", "Approximately Equal"),
            ("σ", r"\sigma", "Activation Function/Sigmoid"),
            ("ϕ", r"\phi", "Feature Map"),
        ]

    @staticmethod
    def get_relation_symbols():
        return [
            ("≡", r"\equiv", "Identical To"),
            ("≡", r"\equiv \pmod{n}", "Congruent Modulo n"),
            ("≃", r"\simeq", "Asymptotically Equal"),
            ("≍", r"\asymp", "Equivalent To"),
            ("≕", r"\coloneq", "Equal By Definition"),
            ("≔", r"\coloneqq", "Equal By Definition (variant)"),
            ("≅", r"\cong", "Congruent To"),
            ("≈", r"\approx", "Approximately Equal"),
            ("≠", r"\neq", "Not Equal"),
            ("≻", r"\succ", "Succeeds"),
            ("≺", r"\prec", "Precedes"),
            ("≼", r"\preceq", "Precedes or Equal"),
            ("≽", r"\succeq", "Succeeds or Equal"),
            ("≤", r"\leq", "Less Than or Equal"),
            ("≥", r"\geq", "Greater Than or Equal"),
            ("≪", r"\ll", "Much Less Than"),
            ("≫", r"\gg", "Much Greater Than"),
            ("∝", r"\propto", "Proportional To"),
            ("≜", r"\triangleq", "Defined As"),
            ("≝", r"\triangleq", "Equal By Definition"),
            ("≐", r"\doteq", "Approaches Limit"),
            ("≙", r"\eqcirc", "Estimates"),
            ("≟", r"\stackrel{?}{=}", "Questioned Equal To"),
            ("≑", r"\doteqdot", "Geometrically Equal"),
            ("≒", r"\fallingdotseq", "Approximately Equal/Congruent"),
        ]

    # 카테고리 정보
    CATEGORIES = [
        ("Lowercase greek letters", "get_lowercase_greek"),
        ("Capital greek letters", "get_uppercase_greek"),
        ("Roman Script Letters", "get_script_letters"),
        ("Math/Engineering Symbols", "get_math_symbols"),
        ("Vector/Matrix Operations", "get_vector_symbols"),
        ("Set theory", "get_set_symbols"),
        ("Logical operations", "get_logic_symbols"),
        ("Probability", "get_stat_symbols"),
        ("Physics", "get_physics_symbols"),
        ("Calculus", "get_calculus_symbols"),
        ("AI/ML", "get_ai_symbols"),
        ("Definition/Equation/Relationship", "get_relation_symbols"),
    ]

    @classmethod
    def get_category_symbols(cls, method_name):
        """카테고리 메서드명으로 심볼 데이터 반환"""
        return getattr(cls, method_name)()
