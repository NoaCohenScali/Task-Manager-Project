from app import app, db
from flask import request, jsonify
from models import Donation, Donator

# GET all donations
@app.route("/api/donations", methods=["GET"])
def get_all_donations():
    donations = Donation.query.all()
    result = [donation.to_json() for donation in donations]
    return jsonify(result)

# GET all donators
@app.route("/api/donators", methods=["GET"])
def get_all_donators():
    donators = Donator.query.all()
    result = [donator.to_json() for donator in donators]
    return jsonify(result)

# create a donator
@app.route("/api/donators", methods=['POST'])
def create_donator():
    try:
        data = request.json

        required_fields = ["first_name", "last_name", "phone", "email", "address"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error":f'Missing field: {field}'}), 400

        first_name = data.get("first_name")
        last_name = data.get("last_name")        
        phone = data.get("phone")
        email = data.get("email")     
        address = data.get("address")   

        new_donator = Donator(first_name=first_name, last_name=last_name, phone=phone, email=email, address=address)

        db.session.add(new_donator)
        db.session.commit()

        return jsonify({"message":"donator created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500    
    
# DELETE a donator
@app.route("/api/donators/<int:id>", methods=["DELETE"])
def delete_donator(id):
    try:
        donator = Donator.query.get(id)

        if donator is None:
            return jsonify({"error":"Donator not found"}), 404

        db.session.delete(donator)
        db.session.commit()

        return jsonify({"message":"Donator deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500

# UPDATE a donator
@app.route("/api/donators/<int:id>", methods=["PATCH"])
def update_donator(id):
    try:
        donator = Donator.query.get(id)

        if donator is None:
            return jsonify({"error":"Donator not found"}), 404
        
        data = request.json
        
        donator.first_name = data.get("first_name", donator.first_name)
        donator.last_name = data.get("last_name", donator.last_name)
        donator.phone = data.get("phone", donator.phone)
        donator.email = data.get("email", donator.email)
        donator.address = data.get("address", donator.address)

        db.session.commit()

        return jsonify({"message":"donator updated successfully"}, donator.to_json())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500

