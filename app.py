from flask import Flask, request, jsonify
from database import engine, SessionLocal, Base
from models import User, Transaction
from datetime import datetime
from risk_engine import calculate_risk
from aml_engine import check_aml
from fraud_model import train_fraud_model

fraud_model = train_fraud_model()

# Create tables
Base.metadata.create_all(bind=engine)

app = Flask(__name__)

@app.route("/")
def home():
    return "SmartPay Wallet Backend Running"

@app.route("/register", methods=["POST"])
def register():
    session = SessionLocal()
    data = request.json

    try:
        user = User(
            name=data["name"],
            email=data["email"],
            mobile=data["mobile"]
        )

        session.add(user)
        session.commit()

        return jsonify({"message": "User registered successfully"})

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)})

    finally:
        session.close()




@app.route("/add_money", methods=["POST"])
def add_money():
    session = SessionLocal()
    data = request.json

    try:
        user = session.query(User).filter(User.id == data["user_id"]).first()

        if not user:
            return jsonify({"error": "User not found"})

        user.wallet_balance += float(data["amount"])
        session.commit()

        return jsonify({
            "message": "Money added successfully",
            "new_balance": user.wallet_balance
        })

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)})

    finally:
        session.close()



@app.route("/balance/<int:user_id>", methods=["GET"])
def check_balance(user_id):
    session = SessionLocal()

    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        return jsonify({"error": "User not found"})

    return jsonify({
        "user": user.name,
        "wallet_balance": user.wallet_balance
    })


@app.route("/transfer", methods=["POST"])
def transfer():
    session = SessionLocal()
    data = request.json

    try:
        sender = session.query(User).filter(User.id == data["sender_id"]).first()
        receiver = session.query(User).filter(User.id == data["receiver_id"]).first()

        if not sender or not receiver:
            return jsonify({"error": "Invalid sender or receiver"})

        amount = float(data["amount"])

        if sender.wallet_balance < amount:
            return jsonify({"error": "Insufficient balance"})

        # -------- RISK ENGINE --------
        device_change = data.get("device_change", False)
        otp_failures = data.get("otp_failures", 0)

        risk_score, risk_category = calculate_risk(
            amount, device_change, otp_failures
        )

        # -------- FRAUD MODEL --------
        ml_input = [[amount, int(device_change), otp_failures]]
        ml_prediction = fraud_model.predict(ml_input)[0]
        ml_probability = fraud_model.predict_proba(ml_input)[0][1]


        # -------- AML ENGINE --------
        country = data.get("country", "India")

        previous_txns_count = session.query(Transaction).filter(
            Transaction.sender_id == sender.id,
            Transaction.receiver_id == receiver.id
        ).count()

        aml_flags = check_aml(amount, country, previous_txns_count)

        # If AML flags exist → mark fraud_flag = 1
        fraud_flag = 1 if (aml_flags or ml_prediction == 1) else 0

        # -------- PROCESS TRANSACTION --------
        sender.wallet_balance -= amount
        receiver.wallet_balance += amount

        txn = Transaction(
            sender_id=sender.id,
            receiver_id=receiver.id,
            amount=amount,
            txn_type="P2P",
            country=country,
            risk_score=risk_score,
            fraud_flag=fraud_flag
        )

        session.add(txn)
        session.commit()

        return jsonify({
            "message": "Transfer processed",
            "risk_score": risk_score,
            "risk_category": risk_category,
            "aml_flags": aml_flags,
            "ml_fraud_prediction": int(ml_prediction),
            "ml_fraud_probability": float(ml_probability),
            "fraud_flag": fraud_flag,
            "sender_balance": sender.wallet_balance
        })

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)})

    finally:
        session.close()











if __name__ == "__main__":
    app.run(debug=True)
