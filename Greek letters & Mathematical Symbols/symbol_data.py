# symbol_data.py
"""
기본 심볼 데이터 (그리스 문자만) 및 커스텀 심볼 관리
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

    # 기본 고정 카테고리 (그리스 문자만)
    FIXED_CATEGORIES = [
        ("Lowercase greek letters", "get_lowercase_greek"),
        ("Capital greek letters", "get_uppercase_greek"),
    ]

    @classmethod
    def get_category_symbols(cls, method_name):
        """카테고리 메서드명으로 심볼 데이터 반환"""
        return getattr(cls, method_name)()

    @classmethod
    def get_all_categories(cls, custom_categories=None):
        """고정 카테고리 + 커스텀 카테고리 반환"""
        all_categories = list(cls.FIXED_CATEGORIES)

        if custom_categories:
            for custom_cat in custom_categories:
                category_info = custom_cat.get("category_info", {})
                name = category_info.get("name", "Unknown Category")
                # 커스텀 카테고리는 특별한 식별자 사용
                all_categories.append(
                    (name, f"custom_{custom_cat.get('_filename', '')}", custom_cat)
                )

        return all_categories

    @classmethod
    def get_custom_category_symbols(cls, custom_data):
        """커스텀 카테고리의 심볼 데이터 반환"""
        symbols = custom_data.get("symbols", [])
        return [(s["symbol"], s["latex"], s["name"]) for s in symbols]
