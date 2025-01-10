from flask import Flask, render_template, request
import csv
import random

app = Flask(__name__)

# Pythonの enumerate を Jinja2 テンプレートで使えるようにする
app.jinja_env.globals.update(enumerate=enumerate)


def load_questions(file_path):
    """CSVファイルからクイズデータを読み込む"""
    questions = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append({
                "question": row["question"],
                "options": [row["option1"], row["option2"], row["option3"], row["option4"]],
                "answer": int(row["answer"]) - 1  # インデックスを0ベースに変換
            })
    return questions

questions = load_questions("questions.csv")
random.shuffle(questions)  # 問題をランダムにシャッフル

@app.route("/")
def home():
    """ホームページ（最初のクイズ画面）"""
    return render_template("quiz.html", question=questions[0], index=0, score=0)

@app.route("/answer", methods=["POST"])
def answer():
    """回答処理"""
    index = int(request.form["index"])
    selected = int(request.form["selected"])
    score = int(request.form["score"])

    correct = questions[index]["answer"]
    next_index = index + 1
    is_correct = (selected == correct)

    if is_correct:
        score += 1

    if next_index < len(questions):
        return render_template(
            "quiz.html", 
            question=questions[next_index], 
            index=next_index, 
            score=score, 
            feedback="正解！" if is_correct else "不正解..."
        )
    else:
        return render_template("result.html", score=score, total=len(questions))

if __name__ == "__main__":
    app.run(debug=True)
