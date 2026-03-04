import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

# -----------------------------
# Label mapping (your commands)
# -----------------------------
LABELS = [0, 1, 2, 3]
LABEL_NAMES = ["Forward", "Backward", "Left", "Right"]
label_to_name = {i: n for i, n in zip(LABELS, LABEL_NAMES)}

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("Dataset.csv")  # update path if needed

assert "class" in df.columns, "Expected target column named 'class'"

X = df.drop(columns=["class"])
y = df["class"].astype(int)

print("Shape:", df.shape)
print("\nClass distribution:\n", y.value_counts().sort_index().rename(index=label_to_name))

# -----------------------------
# Preprocessing (EEG-friendly)
# log1p on band power columns
# -----------------------------
log_cols = ["Delta","Theta","Alpha1","Alpha2","Beta1","Beta2","Gamma1","Gamma2","totPwr"]
pass_cols = [c for c in X.columns if c not in log_cols]

preprocess = ColumnTransformer(
    transformers=[
        ("log", FunctionTransformer(np.log1p, validate=False), log_cols),
        ("pass", "passthrough", pass_cols),
    ],
    remainder="drop"
)

# -----------------------------
# Train/test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ============================================================
# 1) Linear SVM baseline (fast, good starting point)
# ============================================================
linear_svm = Pipeline(steps=[
    ("pre", preprocess),
    ("scaler", StandardScaler()),
    ("clf", LinearSVC(class_weight="balanced", max_iter=30000, dual="auto"))
])

linear_svm.fit(X_train, y_train)
pred = linear_svm.predict(X_test)

print("\n================ Linear SVM ================")
print("Accuracy:", accuracy_score(y_test, pred))
print("Macro F1:", f1_score(y_test, pred, average="macro"))
print("Confusion matrix:\n", confusion_matrix(y_test, pred, labels=LABELS))
print("\nReport:\n", classification_report(
    y_test, pred,
    labels=LABELS,
    target_names=LABEL_NAMES,
    digits=3
))

# ============================================================
# 2) Tuned RBF SVM (more expressive; use for better accuracy)
#    Includes probability output for confidence thresholding
# ============================================================
rbf_svm = Pipeline(steps=[
    ("pre", preprocess),
    ("scaler", StandardScaler()),
    ("clf", SVC(kernel="rbf", class_weight="balanced", probability=True))
])

param_grid = {
    "clf__C": [0.1, 1, 10, 50],
    "clf__gamma": ["scale", 0.01, 0.1, 1],
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

grid = GridSearchCV(
    rbf_svm,
    param_grid=param_grid,
    scoring="f1_macro",   # better for imbalanced multiclass
    cv=cv,
    n_jobs=-1
)

grid.fit(X_train, y_train)
best_model = grid.best_estimator_

pred2 = best_model.predict(X_test)

print("\n================ Tuned RBF SVM ================")
print("Best params:", grid.best_params_)
print("Accuracy:", accuracy_score(y_test, pred2))
print("Macro F1:", f1_score(y_test, pred2, average="macro"))
print("Confusion matrix:\n", confusion_matrix(y_test, pred2, labels=LABELS))
print("\nReport:\n", classification_report(
    y_test, pred2,
    labels=LABELS,
    target_names=LABEL_NAMES,
    digits=3
))

# ============================================================
# 3) Safety layer: confidence threshold + smoothing window
#    - If model isn't confident, output "STOP" (or "HOLD")
#    - Smooth commands with majority vote in last N samples
# ============================================================
def safe_predict_stream(model, X_stream: pd.DataFrame, prob_threshold=0.65, window=5):
    """
    model: trained Pipeline with SVC(probability=True)
    X_stream: streaming features (rows in time order)
    prob_threshold: reject if max prob below this
    window: majority vote window size
    """
    probs = model.predict_proba(X_stream)  # shape (n, 4)
    raw = probs.argmax(axis=1)             # predicted class
    conf = probs.max(axis=1)               # confidence

    safe_cmds = []
    history = []

    for cls, c in zip(raw, conf):
        if c < prob_threshold:
            cmd = "STOP"   # safest fallback
        else:
            cmd = label_to_name[int(cls)]

        history.append(cmd)
        if len(history) > window:
            history.pop(0)

        # Majority vote smoothing, ignoring STOP only if you want:
        # Here: include STOP in vote so low confidence can dominate (safer).
        values, counts = np.unique(history, return_counts=True)
        smoothed = values[np.argmax(counts)]
        safe_cmds.append((cmd, float(c), smoothed))

    return safe_cmds

demo = safe_predict_stream(best_model, X_test.iloc[:30], prob_threshold=0.70, window=7)

print("\n--- Safety-layer demo (first 10 stream outputs) ---")
for i, (cmd, conf, smooth) in enumerate(demo[:10]):
    print(f"{i:02d} raw={cmd:8s} conf={conf:.3f}  ->  smoothed={smooth}")
