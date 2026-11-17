# NumPy Deep Dive — From Recognition to Depth

> **Goal:** Turn my typed-along `Numpy.ipynb` (recognition-level) into real depth.
> **Rule:** No NEW topics. Same syllabus, deeper layer.
> **Time:** ~45–60 min/day, 5–7 days. During TEE week: max 30 min/day or skip.

---

## Step 0 — Inventory (30 min, once)

Open `Numpy.ipynb` and list every concept it covers. This is the syllabus.
Whatever I can't explain out loud later becomes a weak spot.

- [ ] Array creation — `array`, `zeros`, `ones`, `full`, `random`, `arange`
- [ ] Attributes — `shape`, `ndim`, `size`, `dtype`
- [ ] Reshape — `reshape`, `flatten`, `ravel`
- [ ] Transpose — `.T`
- [ ] Indexing & slicing — 1D, 2D, negative indices, step
- [ ] Sorting — `np.sort`, descending
- [ ] Axis logic — `axis=0` vs `axis=1`
- [ ] Stacking / joining
- [ ] Vectorized math & broadcasting

---

## Step 1 — Blank-Page Dump (Day 1) 🧠

New empty notebook. **Notes closed, tutorial closed, Google closed.**

Write from pure memory: create a 2D array, slice it, reshape it, sort it, sum by axis.
Ugly is fine — wrong is informative.

**Output:** a list titled `WEAK SPOTS` — everything I couldn't recall or got wrong.
This list, not the tutorial, drives the rest of the week.

---

## Step 2 — The "Why" Experiments (Day 2–3) 🔬

For each weak spot, don't re-watch. **Run one experiment that answers "why".**

1. **Vectorization** — sum of 10 million numbers: Python `for` loop vs `np.sum()`.
   Time both with `%timeit`. See the speed gap with my own eyes. This is *why* NumPy exists.
2. **Views vs copies** — my notebook says "ravel() returns original instead of copy". Prove it:
   `r = reshaped.ravel(); r[0] = 999` → did `reshaped` change? Then try the same with `flatten()`.
   Slicing does the same thing (`a[0:3]` is a view too). Understand *memory*, not syntax.
3. **Axis logic** — before running, **predict on paper** what `arr.sum(axis=0)` and `axis=1`
   give for a (3,4) array. Verify. Repeat until prediction is always right.
4. **dtypes** — an image is `uint8`. What is `np.uint8(255) + np.uint8(1)`? (Overflow!)
   Connects directly to my CNN projects.
5. **Broadcasting** — `(3,1) + (1,4)` → what shape? Draw it as a grid, then verify.

---

## Step 3 — Drills (Day 3–5) 🏋️

Solve in a fresh notebook, **struggle first, look up only after being stuck.**
Two numbers per drill: easy warm-up → connects to my AI journey.

1. Identity matrix 4x4 → `np.eye(4)`
2. `arange(0,50)` reshaped to (5,10) → row/col sums
3. Random (5,4): mean, std, min, max **per row and per column** (axis!)
4. Boolean mask: all values above the array's mean
5. Replace `NaN`s with the column mean
6. Min-max normalize one column to [0,1] — by hand
7. Z-score standardize by hand — this IS sklearn's `StandardScaler`
8. Sort a 2D array by its 2nd column (`argsort`)
9. Stack two arrays horizontally and vertically
10. Extract the diagonal and anti-diagonal
11. Swap row 0 and row 2 with fancy indexing (no temp variable)
12. **Cosine similarity** between two vectors, from scratch — this is RAG retrieval
13. **One-hot encode** integer labels by hand — this is ML preprocessing
14. **ReLU** with `np.maximum(arr, 0)` — this is deep learning
15. **Softmax** with `axis=1, keepdims=True` — this lives inside attention
16. Moving average with a sliding window
17. Unique rows of a 2D array
18. Load any image → flip horizontally, crop center, plot (images = arrays)

---

## Step 4 — One Mini Build (Day 6, pick ONE) 🛠️

Depth test = using NumPy to build something real, from memory:

- **A.** `StandardScaler` + `MinMaxScaler` class from scratch, tested on a Kaggle CSV,
  compared against sklearn's output → "I know what sklearn does inside."
- **B.** `dl_primitives.ipynb` — one-hot, ReLU, softmax, z-score, cosine similarity,
  each in <10 lines of NumPy → "I know the primitives my DL models use."
- **C.** Image lab — load, flip, crop, channel-separate a photo → "I know why CNN
  input shape is (H, W, C)."

---

## Step 5 — Teach It Back + Store (Day 7) 📝

- Write `numpy_depth_note.md` **in my own words**: what an ndarray really is,
  views vs copies, axis logic, broadcasting rules, dtypes — plus the 5 mistakes I made.
- Explain the whole thing out loud in Hindi/English, as if teaching a friend.
- Add it to this folder, commit: `git commit -m "NumPy deep dive: depth note + drills"`

---

## ✅ Depth Test (pass = done)

- [ ] Explained views vs copies with an example, without notes
- [ ] Predicted `axis=0/1` results correctly on paper, 5/5 times
- [ ] Built 3+ AI primitives (one-hot / ReLU / softmax / cosine sim) from memory
- [ ] Empty notebook → working NumPy code in 10 minutes, zero lookups

---

## ♻️ Reusable Template (copy for next topic)

1. **Inventory** — list what my existing notes cover
2. **Blank-page dump** — find weak spots by failing from memory
3. **Why experiments** — one tiny experiment per weak spot
4. **Drills** — 15–20 problems, struggle first
5. **Mini build** — one small real application, connected to my AI journey
6. **Teach back + depth note** — own words, then commit

Next candidates (one at a time!): Pandas → train/test split & metrics → gradient descent → attention
