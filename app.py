import csv
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# 1セッションあたりの問題数
QUESTIONS_PER_SESSION = 30

# CSVファイルから問題データを読み込む関数
def load_questions():
    questions = []
    with open('questions.csv', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append({
                "question": row["question"],
                "choices": [row["choice1"], row["choice2"], row["choice3"], row["choice4"]],
                "answer": int(row["answer"]) - 1  # インデックスを0ベースに変換
            })
    return questions


# 問題データをCSVから読み込む
questions = load_questions()
total_questions = len(questions)

@app.route("/")
def index():
    # クイズの問題セットを計算する
    sets = [
        (i * QUESTIONS_PER_SESSION, min((i + 1) * QUESTIONS_PER_SESSION - 1, total_questions - 1))
        for i in range((total_questions + QUESTIONS_PER_SESSION - 1) // QUESTIONS_PER_SESSION)
    ]
    # index.htmlにsetsを渡してレンダリング
    return render_template("index.html", sets=sets, QUESTIONS_PER_SESSION=QUESTIONS_PER_SESSION)

@app.route("/quiz/<int:set_id>", methods=["GET", "POST"])
def quiz(set_id):
    # 出題する問題セットの開始・終了インデックスを計算
    start_index = (set_id - 1) * QUESTIONS_PER_SESSION
    end_index = min(start_index + QUESTIONS_PER_SESSION, len(questions))
    question_set = questions[start_index:end_index]

    if request.method == "POST":
        # ユーザーが送信した解答を取得
        user_answers = request.form.getlist("answers")
        score = sum(1 for i, ans in enumerate(user_answers) if ans and int(ans) == question_set[i]["answer"])
        return render_template("result.html", score=score, total=len(question_set), set_id=set_id)
    
    # GETリクエストで問題を表示
    return render_template("quiz.html", question_set=question_set, set_id=set_id, total=len(question_set), enumerate = enumerate)

if __name__ == "__main__":
    app.run(debug=True)
