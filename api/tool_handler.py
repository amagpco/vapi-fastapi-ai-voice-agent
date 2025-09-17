from core.config import appointments_collection, slots_collection
from types.services import (
    cancel_user_appointment, 
    check_user_appointments, 
    create_user_appointment, 
    get_available_slots, 
    reschedule_user_appointment
)

# ------------------------------------------------------------------------
# handle_tool_call: A dispatcher function to handle different tool calls
# ------------------------------------------------------------------------
# This function receives the `name` of the tool to execute and a dictionary
# of `args` as parameters. Based on the `name`, it calls the corresponding
# service function and returns the result.
#
# Tools supported:
#   - check_user_appointments
#   - create_user_appointment
#   - reschedule_user_appointment
#   - cancel_user_appointment
#   - get_available_slots
#
# If the tool name is unknown, an error dictionary is returned.
# ------------------------------------------------------------------------
async def handle_tool_call(name, args):
    # --------------------------------------------------------------------
    # Check user's existing appointments
    # --------------------------------------------------------------------
    if name == "check_user_appointments":
        result = await check_user_appointments(
            collection=appointments_collection, 
            user_number=args['user_number'], 
            user_name=args['user_name']
        )
        return result

    # --------------------------------------------------------------------
    # Create a new appointment for the user
    # --------------------------------------------------------------------
    elif name == "create_user_appointment":
        result = await create_user_appointment(
            collection=appointments_collection,
            user_name=args['user_name'], 
            user_number=args['user_number'],
            service_type=args['service_type'],
            preferred_date=args['preferred_date'],
            preferred_time=args['preferred_time']
        )
        return result

    # --------------------------------------------------------------------
    # Reschedule an existing appointment (update date & time)
    # --------------------------------------------------------------------
    elif name == "reschedule_user_appointment":
        result = await reschedule_user_appointment(
            collection=appointments_collection, 
            appointment_id=args['appointment_id'], 
            new_date=args['new_date'], 
            new_time=args['new_time']
        )
        # Note: We are returning a custom response instead of `result`
        return {
            "success": True,
            "appointment_id": args["appointment_id"],
            "new_date": args["new_date"],
            "new_time": args["new_time"],
            "status": "rescheduled"
        }

    # --------------------------------------------------------------------
    # Cancel an appointment based on appointment_id
    # --------------------------------------------------------------------
    elif name == "cancel_user_appointment":
        result = await cancel_user_appointment(
            collection=appointments_collection, 
            appointment_id=args['appointment_id']
        )
        return result

    # --------------------------------------------------------------------
    # Fetch available slots for a service on a given date
    # --------------------------------------------------------------------
    elif name == "get_available_slots":
        result = await get_available_slots(
            collection=slots_collection, 
            service_type=args['service_type'], 
            date=args['date']
        )
        return result

    # --------------------------------------------------------------------
    # Unknown tool name -> return error
    # --------------------------------------------------------------------
    else:
        return {"error": f"Unknown tool: {name}"}
