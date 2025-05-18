#NoEnv
#SingleInstance, Force
SendMode Input
SetWorkingDir %A_ScriptDir%

; 최근 사용된 문자 배열 초기화 (최대 5개 저장)
global recentSymbols := []
global vButton0, vButton1, vButton2, vButton3, vButton4, vButton5, vButton6, vButton7, vButton8, vButton9, vButton10, vButton11, vButton12, vButton13, vButton14, vButton15

; Alt+G를 누르면 그리스 문자 메뉴 표시
!g::
    ; 현재 마우스 위치 저장
    MouseGetPos, mouseX, mouseY
    
    ; 그리스 문자 하위 메뉴 추가
    Menu, GreekSubmenu, Add, α (alpha), PasteGreekLetter
    Menu, GreekSubmenu, Add, β (beta), PasteGreekLetter
    Menu, GreekSubmenu, Add, γ (gamma), PasteGreekLetter
    Menu, GreekSubmenu, Add, δ (delta), PasteGreekLetter
    Menu, GreekSubmenu, Add, ε (epsilon), PasteGreekLetter
    Menu, GreekSubmenu, Add, ζ (zeta), PasteGreekLetter
    Menu, GreekSubmenu, Add, η (eta), PasteGreekLetter
    Menu, GreekSubmenu, Add, θ (theta), PasteGreekLetter
    Menu, GreekSubmenu, Add, ι (iota), PasteGreekLetter
    Menu, GreekSubmenu, Add, κ (kappa), PasteGreekLetter
    Menu, GreekSubmenu, Add, λ (lambda), PasteGreekLetter
    Menu, GreekSubmenu, Add, μ (mu), PasteGreekLetter
    Menu, GreekSubmenu, Add, ν (nu), PasteGreekLetter
    Menu, GreekSubmenu, Add, ξ (xi), PasteGreekLetter
    Menu, GreekSubmenu, Add, ο (omicron), PasteGreekLetter
    Menu, GreekSubmenu, Add, π (pi), PasteGreekLetter
    Menu, GreekSubmenu, Add, ρ (rho), PasteGreekLetter
    Menu, GreekSubmenu, Add, σ (sigma), PasteGreekLetter
    Menu, GreekSubmenu, Add, τ (tau), PasteGreekLetter
    Menu, GreekSubmenu, Add, υ (upsilon), PasteGreekLetter
    Menu, GreekSubmenu, Add, φ (phi), PasteGreekLetter
    Menu, GreekSubmenu, Add, χ (chi), PasteGreekLetter
    Menu, GreekSubmenu, Add, ψ (psi), PasteGreekLetter
    Menu, GreekSubmenu, Add, ω (omega), PasteGreekLetter
    
    ; 대문자 그리스 문자 추가
    Menu, GreekSubmenuUpper, Add, Α (Alpha), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Β (Beta), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Γ (Gamma), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Δ (Delta), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Ε (Epsilon), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Ζ (Zeta), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Η (Eta), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Θ (Theta), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Ι (Iota), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Κ (Kappa), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Λ (Lambda), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Μ (Mu), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Ν (Nu), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Ξ (Xi), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Ο (Omicron), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Π (Pi), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Ρ (Rho), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Σ (Sigma), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Τ (Tau), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Υ (Upsilon), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Φ (Phi), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Χ (Chi), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Ψ (Psi), PasteGreekLetter
    Menu, GreekSubmenuUpper, Add, Ω (Omega), PasteGreekLetter
    
    ; 기본 수학/공학 기호 추가
    Menu, MathSubmenu, Add, ∑ (Sum), PasteGreekLetter
    Menu, MathSubmenu, Add, ∏ (Product), PasteGreekLetter
    Menu, MathSubmenu, Add, ∂ (Partial), PasteGreekLetter
    Menu, MathSubmenu, Add, ∇ (Nabla), PasteGreekLetter
    Menu, MathSubmenu, Add, ∞ (Infinity), PasteGreekLetter
    Menu, MathSubmenu, Add, ∫ (Integral), PasteGreekLetter
    Menu, MathSubmenu, Add, ≈ (Approximately), PasteGreekLetter
    Menu, MathSubmenu, Add, ≠ (Not Equal), PasteGreekLetter
    Menu, MathSubmenu, Add, ≤ (Less Than or Equal), PasteGreekLetter
    Menu, MathSubmenu, Add, ≥ (Greater Than or Equal), PasteGreekLetter
    Menu, MathSubmenu, Add, ∈ (Element Of), PasteGreekLetter
    Menu, MathSubmenu, Add, ⊂ (Subset), PasteGreekLetter
    Menu, MathSubmenu, Add, ∩ (Intersection), PasteGreekLetter
    Menu, MathSubmenu, Add, ∪ (Union), PasteGreekLetter
    Menu, MathSubmenu, Add, → (Right Arrow), PasteGreekLetter
    Menu, MathSubmenu, Add, ← (Left Arrow), PasteGreekLetter
    Menu, MathSubmenu, Add, ↔ (Double Arrow), PasteGreekLetter
    Menu, MathSubmenu, Add, ≡ (Identical To), PasteGreekLetter
    Menu, MathSubmenu, Add, ≅ (Congruent To), PasteGreekLetter
    Menu, MathSubmenu, Add, ≜ (Defined As), PasteGreekLetter
    
    ; 벡터/행렬 연산 기호 추가
    Menu, VectorSubmenu, Add, · (Dot Product), PasteGreekLetter
    Menu, VectorSubmenu, Add, × (Cross Product), PasteGreekLetter
    Menu, VectorSubmenu, Add, ⊗ (Tensor Product), PasteGreekLetter
    Menu, VectorSubmenu, Add, ⊕ (Direct Sum), PasteGreekLetter
    Menu, VectorSubmenu, Add, ⟨ (Left Angle Bracket), PasteGreekLetter
    Menu, VectorSubmenu, Add, ⟩ (Right Angle Bracket), PasteGreekLetter
    Menu, VectorSubmenu, Add, ‖ (Norm), PasteGreekLetter
    Menu, VectorSubmenu, Add, ⊥ (Perpendicular), PasteGreekLetter
    Menu, VectorSubmenu, Add, ∥ (Parallel), PasteGreekLetter
    Menu, VectorSubmenu, Add, † (Conjugate Transpose), PasteGreekLetter
    Menu, VectorSubmenu, Add, ⊙ (Hadamard/Element-wise Product), PasteGreekLetter
    Menu, VectorSubmenu, Add, ⨂ (Kronecker Product), PasteGreekLetter
    Menu, VectorSubmenu, Add, ⨁ (Direct Sum Operator), PasteGreekLetter
    Menu, VectorSubmenu, Add, ⟦ (Left Double Bracket), PasteGreekLetter
    Menu, VectorSubmenu, Add, ⟧ (Right Double Bracket), PasteGreekLetter
    
    ; 집합 이론 기호 추가
    Menu, SetSubmenu, Add, ∅ (Empty Set), PasteGreekLetter
    Menu, SetSubmenu, Add, ∀ (For All), PasteGreekLetter
    Menu, SetSubmenu, Add, ∃ (There Exists), PasteGreekLetter
    Menu, SetSubmenu, Add, ∄ (Does Not Exist), PasteGreekLetter
    Menu, SetSubmenu, Add, ∉ (Not Element Of), PasteGreekLetter
    Menu, SetSubmenu, Add, ⊄ (Not Subset), PasteGreekLetter
    Menu, SetSubmenu, Add, ⊆ (Subset or Equal), PasteGreekLetter
    Menu, SetSubmenu, Add, ⊇ (Superset or Equal), PasteGreekLetter
    Menu, SetSubmenu, Add, ⊊ (Proper Subset), PasteGreekLetter
    Menu, SetSubmenu, Add, ⊋ (Proper Superset), PasteGreekLetter
    Menu, SetSubmenu, Add, ℕ (Natural Numbers), PasteGreekLetter
    Menu, SetSubmenu, Add, ℤ (Integers), PasteGreekLetter
    Menu, SetSubmenu, Add, ℚ (Rational Numbers), PasteGreekLetter
    Menu, SetSubmenu, Add, ℝ (Real Numbers), PasteGreekLetter
    Menu, SetSubmenu, Add, ℂ (Complex Numbers), PasteGreekLetter
    Menu, SetSubmenu, Add, ℙ (Prime Numbers), PasteGreekLetter
    Menu, SetSubmenu, Add, △ (Symmetric Difference), PasteGreekLetter
    Menu, SetSubmenu, Add, × (Cartesian Product), PasteGreekLetter
    
    ; 논리 연산 기호 추가
    Menu, LogicSubmenu, Add, ¬ (Negation/Not), PasteGreekLetter
    Menu, LogicSubmenu, Add, ∧ (Logical And), PasteGreekLetter
    Menu, LogicSubmenu, Add, ∨ (Logical Or), PasteGreekLetter
    Menu, LogicSubmenu, Add, ⊻ (Exclusive Or), PasteGreekLetter
    Menu, LogicSubmenu, Add, ⇒ (Implies), PasteGreekLetter
    Menu, LogicSubmenu, Add, ⇔ (If and Only If), PasteGreekLetter
    Menu, LogicSubmenu, Add, ⊨ (Models/Entails), PasteGreekLetter
    Menu, LogicSubmenu, Add, ⊢ (Proves), PasteGreekLetter
    Menu, LogicSubmenu, Add, □ (Necessary), PasteGreekLetter
    Menu, LogicSubmenu, Add, ◊ (Possible), PasteGreekLetter
    Menu, LogicSubmenu, Add, ⊤ (Top/True), PasteGreekLetter
    Menu, LogicSubmenu, Add, ⊥ (Bottom/False), PasteGreekLetter
    Menu, LogicSubmenu, Add, ≡ (Logical Equivalence), PasteGreekLetter
    Menu, LogicSubmenu, Add, ⊦ (Assertion), PasteGreekLetter
    
    ; 확률/통계 기호 추가
    Menu, StatSubmenu, Add, 𝔼 (Expected Value), PasteGreekLetter
    Menu, StatSubmenu, Add, ℙ (Probability), PasteGreekLetter
    Menu, StatSubmenu, Add, 𝕍 (Variance), PasteGreekLetter
    Menu, StatSubmenu, Add, √ (Square Root), PasteGreekLetter
    Menu, StatSubmenu, Add, ∝ (Proportional To), PasteGreekLetter
    Menu, StatSubmenu, Add, ± (Plus-Minus), PasteGreekLetter
    Menu, StatSubmenu, Add, ∼ (Distributed As), PasteGreekLetter
    Menu, StatSubmenu, Add, ≫ (Much Greater Than), PasteGreekLetter
    Menu, StatSubmenu, Add, ≪ (Much Less Than), PasteGreekLetter
    Menu, StatSubmenu, Add, μ̂ (mu hat - estimator), PasteGreekLetter
    Menu, StatSubmenu, Add, σ̂ (sigma hat - estimator), PasteGreekLetter
    Menu, StatSubmenu, Add, ρ (rho - correlation), PasteGreekLetter
    Menu, StatSubmenu, Add, χ² (Chi-Squared), PasteGreekLetter
    Menu, StatSubmenu, Add, σ² (Variance), PasteGreekLetter
    Menu, StatSubmenu, Add, ⟂ (Independent), PasteGreekLetter
    Menu, StatSubmenu, Add, ∩ (Intersection/And), PasteGreekLetter
    Menu, StatSubmenu, Add, ∪ (Union/Or), PasteGreekLetter
    
    ; 물리/양자역학 기호 추가
    Menu, PhysicsSubmenu, Add, ℏ (h-bar), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, ψ (wavefunction), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, Ψ (Wavefunction), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, ⟨ϕ|ψ⟩ (Bracket Notation), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, ⊗ (Tensor Product), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, † (Hermitian Conjugate), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, ° (Degree), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, ∮ (Contour Integral), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, ∯ (Surface Integral), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, ∰ (Volume Integral), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, ∇² (Laplacian), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, × (Curl Operator), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, γ (Lorentz Factor), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, Λ (Lambda/Cosmological Constant), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, ⟨Â⟩ (Expectation Value), PasteGreekLetter
    Menu, PhysicsSubmenu, Add, ⨂ (Tensor Product Operator), PasteGreekLetter
    
    ; 미적분학 기호 추가
    Menu, CalculusSubmenu, Add, ∫ (Indefinite Integral), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ∬ (Double Integral), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ∭ (Triple Integral), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ∮ (Contour Integral), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ∯ (Surface Integral), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ∰ (Volume Integral), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ∂x (Partial wrt x), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ∂y (Partial wrt y), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ∂z (Partial wrt z), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ∂t (Partial wrt t), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ′ (Prime/Derivative), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ″ (Double Prime), PasteGreekLetter
    Menu, CalculusSubmenu, Add, dx (Differential x), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ∇f (Gradient), PasteGreekLetter
    Menu, CalculusSubmenu, Add, lim (Limit), PasteGreekLetter
    Menu, CalculusSubmenu, Add, δ (Variation/Functional Derivative), PasteGreekLetter
    Menu, CalculusSubmenu, Add, ε (Epsilon/Small Quantity), PasteGreekLetter
    
    ; AI/머신러닝 기호 추가
    Menu, AISubmenu, Add, ∇θ (Gradient wrt Parameters), PasteGreekLetter
    Menu, AISubmenu, Add, ∑ (Summation), PasteGreekLetter
    Menu, AISubmenu, Add, ∏ (Product), PasteGreekLetter
    Menu, AISubmenu, Add, 𝔼 (Expected Value), PasteGreekLetter
    Menu, AISubmenu, Add, ℙ (Probability), PasteGreekLetter
    Menu, AISubmenu, Add, 𝕍 (Variance), PasteGreekLetter
    Menu, AISubmenu, Add, ⊗ (Tensor Product), PasteGreekLetter
    Menu, AISubmenu, Add, ⊕ (Direct Sum), PasteGreekLetter
    Menu, AISubmenu, Add, ⊙ (Hadamard Product), PasteGreekLetter
    Menu, AISubmenu, Add, ∥W∥ (Norm of Weights), PasteGreekLetter
    Menu, AISubmenu, Add, θ̂ (Parameter Estimate), PasteGreekLetter
    Menu, AISubmenu, Add, ŷ (Prediction), PasteGreekLetter
    Menu, AISubmenu, Add, 𝓛 (Loss Function), PasteGreekLetter
    Menu, AISubmenu, Add, ∂𝓛/∂θ (Gradient of Loss), PasteGreekLetter
    Menu, AISubmenu, Add, ≈ (Approximately Equal), PasteGreekLetter
    Menu, AISubmenu, Add, σ (Activation Function/Sigmoid), PasteGreekLetter
    Menu, AISubmenu, Add, ϕ (Feature Map), PasteGreekLetter
    
    ; 정의/등식/관계 기호 추가
    Menu, RelationSubmenu, Add, ≡ (Identical To), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≅ (Congruent To), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≈ (Approximately Equal), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≠ (Not Equal), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≤ (Less Than or Equal), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≥ (Greater Than or Equal), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≪ (Much Less Than), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≫ (Much Greater Than), PasteGreekLetter
    Menu, RelationSubmenu, Add, ∝ (Proportional To), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≜ (Defined As), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≝ (Equal By Definition), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≐ (Approaches Limit), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≙ (Estimates), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≟ (Questioned Equal To), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≣ (Strictly Equivalent To), PasteGreekLetter
    Menu, RelationSubmenu, Add, ⩵ (Double-Line Equal), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≑ (Geometrically Equal), PasteGreekLetter
    Menu, RelationSubmenu, Add, ≒ (Approximately Equal/Congruent), PasteGreekLetter
    
    ; 메인 컨텍스트 메뉴 설정
    Menu, MyContextMenu, Add, 소문자 그리스 문자, :GreekSubmenu
    Menu, MyContextMenu, Add, 대문자 그리스 문자, :GreekSubmenuUpper
    Menu, MyContextMenu, Add, 수학/공학 기호, :MathSubmenu
    Menu, MyContextMenu, Add, 벡터/행렬 연산, :VectorSubmenu
    Menu, MyContextMenu, Add, 집합 이론, :SetSubmenu
    Menu, MyContextMenu, Add, 논리 연산, :LogicSubmenu
    Menu, MyContextMenu, Add, 확률/통계, :StatSubmenu
    Menu, MyContextMenu, Add, 물리/양자역학, :PhysicsSubmenu
    Menu, MyContextMenu, Add, 미적분학, :CalculusSubmenu
    Menu, MyContextMenu, Add, AI/머신러닝, :AISubmenu
    Menu, MyContextMenu, Add, 정의/등식/관계, :RelationSubmenu
    
    ; 최근 사용 항목이 있으면 추가
    if (recentSymbols.Length() > 0) {
        ; 메인 메뉴에 구분선 추가
        Menu, MyContextMenu, Add
        Menu, MyContextMenu, Add, 최근 사용:, DoNothing
        Menu, MyContextMenu, Disable, 최근 사용:
        
        ; 최근 사용 항목 직접 추가
        for index, item in recentSymbols {
            symbol := item.symbol
            name := item.name
            Menu, MyContextMenu, Add, %symbol% (%name%), PasteRecentLetter
        }
    }
    
    ; 메뉴 표시 (현재 마우스 위치에)
    Menu, MyContextMenu, Show
    
    ; 사용한 메뉴 삭제
    Menu, GreekSubmenu, DeleteAll
    Menu, GreekSubmenuUpper, DeleteAll
    Menu, MathSubmenu, DeleteAll
    Menu, VectorSubmenu, DeleteAll
    Menu, SetSubmenu, DeleteAll
    Menu, LogicSubmenu, DeleteAll
    Menu, StatSubmenu, DeleteAll
    Menu, PhysicsSubmenu, DeleteAll
    Menu, CalculusSubmenu, DeleteAll
    Menu, AISubmenu, DeleteAll
    Menu, RelationSubmenu, DeleteAll
    Menu, MyContextMenu, DeleteAll
return

; 선택된 그리스 문자를 클립보드에 복사하고 붙여넣기
PasteGreekLetter:
    ; 메뉴에서 선택한 항목 가져오기
    fullItem := A_ThisMenuItem
    letter := RegExReplace(fullItem, " \(.*\)$", "")
    name := RegExReplace(fullItem, "^.*? \((.*?)\)$", "$1")
    
    ; 최근 사용에 추가
    AddToRecentSymbols(letter, name)
    
    ; 클립보드에 복사
    clipboard := letter
    
    ; 약간의 지연
    Sleep, 100
    
    ; 붙여넣기 (Ctrl+V)
    SendInput, ^v
return

; 최근 사용 목록에서 선택한 문자 붙여넣기
PasteRecentLetter:
    ; 메뉴에서 선택한 항목 가져오기
    fullItem := A_ThisMenuItem
    letter := RegExReplace(fullItem, " \(.*\)$", "")
    name := RegExReplace(fullItem, "^. \((.*)\)$", "$1")
    
    ; 최근 사용 목록에서 순서 업데이트
    UpdateRecentSymbolOrder(letter)
    
    ; 클립보드에 복사
    clipboard := letter
    
    ; 약간의 지연
    Sleep, 100
    
    ; 붙여넣기 (Ctrl+V)
    SendInput, ^v
return

; 더미 함수 (메뉴 제목용)
DoNothing:
return

; 최근 사용된 기호에 추가
AddToRecentSymbols(letter, name) {
    ; 이미 목록에 있는지 확인
    for index, item in recentSymbols {
        if (item.symbol = letter) {
            ; 이미 있으면 제거 (나중에 맨 앞에 추가)
            recentSymbols.RemoveAt(index)
            break
        }
    }
    
    ; 새 항목을 맨 앞에 추가
    recentSymbols.InsertAt(1, {symbol: letter, name: name})
    
    ; 최대 5개만 유지
    if (recentSymbols.Length() > 5) {
        recentSymbols.Pop()
    }
}

; 최근 사용 목록에서 순서 업데이트
UpdateRecentSymbolOrder(letter) {
    ; 해당 항목 찾기
    for index, item in recentSymbols {
        if (item.symbol = letter) {
            ; 항목 정보 저장
            symbolInfo := item
            ; 목록에서 제거
            recentSymbols.RemoveAt(index)
            ; 맨 앞에 다시 추가
            recentSymbols.InsertAt(1, symbolInfo)
            break
        }
    }
}