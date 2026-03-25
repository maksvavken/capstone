from dataclasses import dataclass
from typing import List

@dataclass
class EvalQ:
    field: str
    style: str
    q: str
    gt: str
    a: str = ""
    math_score: int = 0      # 0-8
    style_score: int = 0     # 0-6
    quality_score: int = 0   # 0-4 (clarity + completeness merged)
    feedback: str = ""

    @property
    def total(self) -> int:
        return self.math_score + self.style_score + self.quality_score


eval_questions: List[EvalQ] = [


    EvalQ(
        field="Algebra",
        style="short_simple",
        q="What does it mean for two expressions to be equivalent?",
        gt="Two expressions are equivalent if they always produce the same value no matter what numbers you substitute in. For example $2(x+3)$ and $2x+6$ are equivalent because multiplying out gives the same result for any $x$.",
    ),
    EvalQ(
        field="Algebra",
        style="short_technical",
        q="Prove that $\\sqrt{2}$ is irrational.",
        gt="Assume $\\sqrt{2} = \\frac{p}{q}$ in lowest terms. Then $2q^2 = p^2$, so $p^2$ is even, hence $p$ is even. Write $p = 2k$; then $2q^2 = 4k^2$, so $q^2 = 2k^2$, making $q$ even — contradicting $\\gcd(p,q)=1$.",
    ),
    EvalQ(
        field="Algebra",
        style="long_simple",
        q="Why does $a^0 = 1$ for any non-zero $a$?",
        gt="Think about the pattern of powers: $a^3 = a \\cdot a \\cdot a$, $a^2 = a \\cdot a$, $a^1 = a$. Each time we decrease the exponent by one we divide by $a$. So going from $a^1$ to $a^0$ means dividing $a$ by $a$, which always gives $1$ as long as $a$ is not zero. Another way to see it: the rule $a^m \\div a^m = a^{m-m} = a^0$ must equal $1$ since anything divided by itself is $1$.",
    ),
    EvalQ(
        field="Algebra",
        style="long_technical",
        q="How to prove $(a-b)^3 + (b-c)^3 + (c-a)^3 - 3(a-b)(b-c)(c-a) = 0$ without calculations?",
        gt="Using the identity $x^3 + y^3 = (x+y)(x^2 - xy + y^2)$, we get $(a-b)^3 + (b-c)^3 = (a-c)((a-b)^2 - (a-b)(b-c) + (b-c)^2)$. Adding $(c-a)^3$ and factoring yields $(c-a)(b-c)(-c+2a-b+a-2b+c) = 3(c-a)(b-c)(a-b)$, hence $(a-b)^3 + (b-c)^3 + (c-a)^3 = 3(a-b)(b-c)(c-a)$.",
    ),

    # -----------------------------------------------------------------------
    # Linear Algebra
    # -----------------------------------------------------------------------
    EvalQ(
        field="Linear Algebra",
        style="step_by_step",
        q="How can I show that $\\begin{pmatrix} 1 & 1 \\\\ 0 & 1\\end{pmatrix}^n = \\begin{pmatrix} 1 & n \\\\ 0 & 1\\end{pmatrix}$?",
        gt="Write the recurrence $x_{n+1} = x_n + y_n$, $y_{n+1} = y_n$. Solving gives $x_n = x_0 + n y_0$, $y_n = y_0$. The first column of $A^n$ uses $x_0=1, y_0=0$ giving $(1\\ 0)^T$. The second column uses $x_0=0, y_0=1$ giving $(n\\ 1)^T$. Hence $A^n = \\begin{pmatrix} 1 & n \\\\ 0 & 1\\end{pmatrix}$.",
    ),
    EvalQ(
        field="Linear Algebra",
        style="short_simple",
        q="What does it mean to say that two vectors are linearly independent?",
        gt="Two vectors are linearly independent if neither one is a scaled version of the other — you cannot get one by stretching or shrinking the other. Imagine two arrows pointing in completely different directions: they are independent. If one is just a longer or shorter version of the other, they are dependent.",
    ),
    EvalQ(
        field="Linear Algebra",
        style="short_technical",
        q="Solve the linear system: $2.6513 = \\frac{3}{2}y + \\frac{x}{2}$ and $1.7675 = y + \\frac{x}{3}$. The variable $x$ seems to cancel when substituting.",
        gt="The coefficient matrix $\\begin{pmatrix} \\frac{1}{2} & \\frac{3}{2} \\\\ \\frac{1}{3} & 1 \\end{pmatrix}$ has $\\det = 0$, so the system is singular. Multiplying out gives $5.3026 = 3y + x$ and $5.3025 = 3y + x$, a contradiction since $5.3026 \\neq 5.3025$. No solution exists.",
    ),
    EvalQ(
        field="Linear Algebra",
        style="long_simple",
        q="What does it mean to say that two vectors are linearly independent, and why does it matter?",
        gt="Two vectors are linearly independent if neither one is a scaled version of the other — that is, you cannot get one by stretching or shrinking the other. Imagine two arrows in a plane: if they point in completely different directions (not parallel), they are independent. If one is just a longer or shorter version of the other, they are dependent. Independent vectors span more directions, which is why independence matters when building a basis for a vector space.",
    ),
    EvalQ(
        field="Linear Algebra",
        style="long_technical",
        q="Prove that $\\det(AB) = \\det(A)\\det(B)$ for square matrices $A$ and $B$.",
        gt="If $A$ is singular, $\\det(A) = 0$ and $AB$ is also singular so both sides are $0$. If $A$ is invertible, express $A$ as a product of elementary matrices $E_1 E_2 \\cdots E_k$. Each elementary matrix $E_i$ satisfies $\\det(E_i B) = \\det(E_i)\\det(B)$ by direct verification for the three row operation types. Applying this inductively gives $\\det(AB) = \\det(E_1)\\cdots\\det(E_k)\\det(B) = \\det(A)\\det(B)$.",
    ),

    # -----------------------------------------------------------------------
    # Calculus
    # -----------------------------------------------------------------------
    EvalQ(
        field="Calculus",
        style="step_by_step",
        q="Show via differentiation that $1 - 2 + 3 - 4 + \\cdots + (-1)^{n-1}n$ equals $-\\frac{n}{2}$ for even $n$ and $\\frac{n+1}{2}$ for odd $n$.",
        gt="Differentiate $\\sum x^k = \\frac{1-x^{n+1}}{1-x}$, set $x=-1$. Result is $\\frac{-2(n+1)(-1)^n + 1 + (-1)^{n+2}}{4}$. For even $n$: $(-1)^n = 1$ gives $\\frac{-2n}{4} = -\\frac{n}{2}$. For odd $n$: $(-1)^n = -1$ gives $\\frac{2n+2}{4} = \\frac{n+1}{2}$.",
    ),
    EvalQ(
        field="Calculus",
        style="short_simple",
        q="Why does the harmonic series $\\sum_{n=1}^\\infty \\frac{1}{n} = \\frac{1}{1} + \\frac{1}{2} + \\frac{1}{3} + \\cdots$ not converge even though it grows very slowly?",
        gt="Group terms in blocks of $9$, $90$, $900$, $\\ldots$ Each block sums to more than $\\frac{9}{10}$, and since there are infinitely many blocks the total sum grows without bound.",
    ),
    EvalQ(
        field="Calculus",
        style="short_technical",
        q="Help with a simple derivative: find $\\dfrac{d}{dx}\\dfrac{6}{\\sqrt{x^3+6}}$.",
        gt="$\\frac{d}{dx}\\frac{6}{\\sqrt{x^3+6}} = 6 \\cdot \\left(-\\frac{1}{2}\\right)(x^3+6)^{-3/2} \\cdot 3x^2 = -\\frac{9x^2}{(x^3+6)^{3/2}}$",
    ),
    EvalQ(
        field="Calculus",
        style="long_simple",
        q="What is the intuition behind the chain rule in differentiation?",
        gt="Imagine you are converting temperature from Celsius to Fahrenheit, and Celsius itself depends on altitude. The chain rule says: if you want to know how fast temperature changes with altitude, multiply how fast Celsius changes with altitude by how fast Fahrenheit changes with Celsius. In math, if $y$ depends on $u$ and $u$ depends on $x$, then $\\frac{dy}{dx} = \\frac{dy}{du} \\cdot \\frac{du}{dx}$. The rates of change multiply together just like unit conversions do.",
    ),
    EvalQ(
        field="Calculus",
        style="long_technical",
        q="Find the $n$-th derivative of $f(x) = e^{1/x}$.",
        gt="By induction, assume $f^{(n-1)}(t) = P_{n-1}\\left(\\frac{1}{t}\\right)f(t)$ for some polynomial $P_{n-1}$. Differentiating gives $f^{(n)}(t) = -\\frac{1}{t^2}\\left\\{P'_{n-1}\\left(\\frac{1}{t}\\right) + P_{n-1}\\left(\\frac{1}{t}\\right)\\right\\}f(t) = P_n\\left(\\frac{1}{t}\\right)f(t)$ where $P_n(x) := x^2[P'_{n-1}(x) - P_{n-1}(x)]$, $P_0 = 1$.",
    ),

    # -----------------------------------------------------------------------
    # Complex Analysis
    # -----------------------------------------------------------------------
    EvalQ(
        field="Complex Analysis",
        style="step_by_step",
        q="Find the Cartesian equation for the locus $|z-1| = 2|z+1|$.",
        gt="Substitute $z = x + iy$, square both sides to get $(x-1)^2 + y^2 = 4((x+1)^2 + y^2)$. Expand and simplify to get $3x^2 + 10x + 3y^2 = -3$, then complete the square to obtain $\\left(x + \\frac{5}{3}\\right)^2 + y^2 = \\frac{16}{9}$, a circle centered at $\\left(-\\frac{5}{3}, 0\\right)$ with radius $\\frac{4}{3}$.",
    ),
    EvalQ(
        field="Complex Analysis",
        style="short_simple",
        q="What does the modulus $|z|$ of a complex number $z = x + iy$ represent geometrically?",
        gt="The modulus $|z| = \\sqrt{x^2 + y^2}$ is simply the distance from the point $(x, y)$ to the origin in the complex plane. It tells you how far the complex number is from zero, just like the length of an arrow from the origin.",
    ),
    EvalQ(
        field="Complex Analysis",
        style="short_technical",
        q="State and briefly explain Euler's formula $e^{i\\theta} = \\cos\\theta + i\\sin\\theta$.",
        gt="Euler's formula follows from comparing the Taylor series: $e^{i\\theta} = \\sum_{n=0}^\\infty \\frac{(i\\theta)^n}{n!} = \\sum_{k=0}^\\infty \\frac{(-1)^k \\theta^{2k}}{(2k)!} + i\\sum_{k=0}^\\infty \\frac{(-1)^k \\theta^{2k+1}}{(2k+1)!} = \\cos\\theta + i\\sin\\theta$.",
    ),
    EvalQ(
        field="Complex Analysis",
        style="long_simple",
        q="What does it mean for a function to be analytic, and why does it matter?",
        gt="A function is analytic at a point if it can be represented by a convergent power series around that point — essentially it is infinitely smooth and well-behaved there. Think of it like a curve with no sharp corners or breaks anywhere you zoom in. Analytic functions are special because knowing their values on even a small region tells you everything about them everywhere (a property called analytic continuation). This makes them incredibly powerful tools in physics, engineering and number theory.",
    ),
    EvalQ(
        field="Complex Analysis",
        style="long_technical",
        q="State Cauchy's integral formula and explain what it implies about analytic functions.",
        gt="If $f$ is analytic inside and on a simple closed contour $C$, and $z_0$ is inside $C$, then $f(z_0) = \\frac{1}{2\\pi i}\\oint_C \\frac{f(z)}{z - z_0}\\,dz$. Differentiating under the integral sign gives $f^{(n)}(z_0) = \\frac{n!}{2\\pi i}\\oint_C \\frac{f(z)}{(z-z_0)^{n+1}}\\,dz$, showing that every analytic function is infinitely differentiable — a property with no analogue in real analysis.",
    ),

    # -----------------------------------------------------------------------
    # Probability
    # -----------------------------------------------------------------------
    EvalQ(
        field="Probability",
        style="step_by_step",
        q="Bowl A has 6 red and 4 blue chips. 5 chips are transferred to Bowl B. One chip drawn from Bowl B is blue. Find $P(\\text{2 red, 3 blue transferred} \\mid \\text{blue drawn})$.",
        gt="$P(A) = \\frac{\\binom{6}{2}\\binom{4}{3}}{\\binom{10}{5}} = \\frac{100}{252}$. $P(B|A) = \\frac{3}{5}$. $P(B) = \\frac{4}{10}$. By Bayes: $P(A|B) = \\frac{(3/5)(100/252)}{4/10} = \\frac{5}{7} \\approx 0.714$.",
    ),
    EvalQ(
        field="Probability",
        style="short_simple",
        q="Box 1 has 10 balls (8 white). Box 2 has 20 balls (4 white). One ball chosen from each box, then one of those two is chosen. Find the probability it is white.",
        gt="Weight cases by $\\frac{1}{2}$ when only one white is available. $P(\\text{white}) = P(ww) + \\frac{1}{2}P(wa) + \\frac{1}{2}P(aw) = \\frac{8}{10}\\cdot\\frac{4}{20} + \\frac{1}{2}\\cdot\\frac{8}{10}\\cdot\\frac{16}{20} + \\frac{1}{2}\\cdot\\frac{2}{10}\\cdot\\frac{4}{20} = 0.5$.",
    ),
    EvalQ(
        field="Probability",
        style="short_technical",
        q="A fair die is tossed until a number greater than 4 appears. What is the probability that an even number of tosses is required?",
        gt="$P(\\text{success on toss } 2k) = \\left(\\frac{2}{3}\\right)^{2k-1}\\frac{1}{3}$. Summing: $\\sum_{k=1}^\\infty \\left(\\frac{2}{3}\\right)^{2k-1}\\frac{1}{3} = \\frac{1}{2}\\cdot\\frac{4/9}{1-4/9} = \\frac{2}{5}$.",
    ),
    EvalQ(
        field="Probability",
        style="long_simple",
        q="If $P(A \\cup B \\cup C) = 1$, $P(B) = 2P(A)$, $P(C) = 3P(A)$, $P(A \\cap B) = P(A \\cap C) = P(B \\cap C)$, prove that $P(A) \\leq \\frac{1}{4}$.",
        gt="Let $x = P((A\\cap B)\\setminus C)$, $y = P(A\\cap B\\cap C)$, and define $a,b,c$ as probabilities of exclusive regions. After substitution $1 = P(A\\cup B\\cup C) = 4P(A) + 2a + x$. Since $2a + x \\geq 0$, we conclude $P(A) \\leq \\frac{1}{4}$.",
    ),
    EvalQ(
        field="Probability",
        style="long_technical",
        q="Is there a general formula for the probability of unbounded cumulative dice rolls hitting a specified number exactly? E.g. with a D6 hitting exactly 14.",
        gt="The probability of hitting sum $n$ is the coefficient of $x^n$ in the generating function $\\frac{6}{6 - x - x^2 - x^3 - x^4 - x^5 - x^6}$, obtained via the geometric series $\\sum_{j=0}^\\infty \\left(\\frac{x+x^2+\\cdots+x^6}{6}\\right)^j$. The coefficient can be extracted using partial fractions applied to the roots of $6 - x - x^2 - x^3 - x^4 - x^5 - x^6 = 0$, or via Cauchy's integral formula.",
    ),
]
