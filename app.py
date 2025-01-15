from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# 問題データの読み込み
def load_questions():
    questions = []
    with open("questions.csv", encoding="shift_jis") as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append({
                "question": row["question"],
                "choices": [row["choice1"], row["choice2"], row["choice3"], row["choice4"]],
                "answer": int(row["answer"]) - 1  # インデックスを0ベースに変換
            })
    return questions

questions = load_questions()

# 1回あたりの問題数
QUESTIONS_PER_SESSION = 30

@app.route("/")
def index():
    # 全問題を30問ごとに分割してセットを作成
    sets = [(i, i + QUESTIONS_PER_SESSION - 1) for i in range(0, len(questions), QUESTIONS_PER_SESSION)]
    return render_template("index.html", sets=sets)

@app.route("/quiz/<int:set_id>", methods=["GET", "POST"])
def quiz(set_id):
    # 問題セットの開始・終了インデックスを計算
    start_index = (set_id - 1) * QUESTIONS_PER_SESSION
    end_index = min(start_index + QUESTIONS_PER_SESSION, len(questions))
    question_set = questions[start_index:end_index]
    
    if request.method == "POST":
        # POSTリクエストで回答が送信された場合
        user_answers = request.form.getlist("answers")
        score = sum(1 for i, ans in enumerate(user_answers) if ans and int(ans) == question_set[i]["answer"])
        return render_template("result.html", score=score, total=len(question_set), set_id=set_id)
    
    # GETリクエストで問題を表示
    return render_template("quiz.html", question_set=question_set, set_id=set_id, total=len(question_set))

@app.route("/result/<int:set_id>")
def result(set_id):
    # 採点結果を表示
    return render_template("result.html", set_id=set_id)

if __name__ == "__main__":
    app.run(debug=True)
