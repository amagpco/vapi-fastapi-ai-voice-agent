import random

async def create_user_appointment(collection, user_name: str, user_number: str, service_type: str, preferred_date: str, preferred_time: str, provider_id: str = None):
    appointment_id = str(random.randint(10000, 99999)) 
    
    appointment = {
        "appointment_id": appointment_id,
        "user_name": user_name,
        "user_number": user_number,
        "service_type": service_type,
        "date": preferred_date,
        "time": preferred_time,
        "provider_id": provider_id or "auto-assigned",
        "status": "confirmed"
    }
    
    result = await collection.insert_one(appointment)
    
    return {
        "success": True,
        "appointment_id": appointment_id,
        "appointment_id": str(result.inserted_id),
        "service_type": service_type,
        "date": preferred_date,
        "time": preferred_time,
        "provider_id": provider_id or "auto-assigned"
    }
    
    
async def reschedule_user_appointment(collection, appointment_id: str, new_date: str, new_time: str):
    result = await collection.update_one(
        {"appointment_id": appointment_id},
        {"$set": {"date": new_date, "time": new_time, "status": "rescheduled"}}
    )
    
    if result.modified_count == 0:
        return {"success": False, "error": "Appointment not found or not modified."}
    
    return {
        "success": True,
        "appointment_id": appointment_id,
        "new_date": new_date,
        "new_time": new_time,
        "status": "rescheduled"
    }
    
async def check_user_appointments(collection, user_number: int, user_name: str):
    appointments_cursor = collection.find(
        {"user_number": user_number}
    )
    appointments = await appointments_cursor.to_list(length=None)

    for appointment in appointments:
        appointment["id"] = str(appointment.pop("_id"))

    return appointments

async def get_available_slots(collection, service_type: str, date: str, provider_id: str = None):
    slots_cursor = collection.find({
        "service_type": service_type,
        "date": date,
        "provider_id": provider_id
    })
    slots = await slots_cursor.to_list(length=None)
    
    available_slots = []
    for slot in slots:
        times = slot.get("available_slots", [])
        available_slots.extend(times)

    return {
        "service_type": service_type,
        "date": date,
        "provider_id": provider_id,
        "available_slots": available_slots
    }
    
async def cancel_user_appointment(collection, appointment_id: str):
    result = await collection.update_one(
        {"appointment_id": appointment_id},
        {"$set": {"status": "cancelled"}}
    )
    
    if result.modified_count == 0:
        return {"success": False, "error": "Appointment not found or already cancelled."}
    
    return {
        "success": True,
        "appointment_id": appointment_id,
        "status": "cancelled"
    }