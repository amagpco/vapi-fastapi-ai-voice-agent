tools = [
    {
        "type": "function",
        "function": {
            "name": "check_user_appointments",
            "description": "Retrieve all upcoming or past appointments for the current user using their phone number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_number": {
                        "type": "string",
                        "description": "The user's phone number in digits only, no spaces or formatting (e.g., '989123456789').",
                        "pattern": "^[0-9]{7,15}$"
                    },
                    "user_name": {
                        "type": "string",
                        "description": "The patient's full name, including first and last name (e.g., 'Sara Johnson')."
                    },
                },
                "required": ["user_number", "user_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_user_appointment",
            "description": "Create a new appointment for the current user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_number": {
                        "type": "string",
                        "description": "The user's phone number in digits only, no spaces or formatting (e.g., '989123456789').",
                        "pattern": "^[0-9]{7,15}$"
                    },
                    "user_name": {
                        "type": "string",
                        "description": "The patient's full name, including first and last name (e.g., 'Sara Johnson')."
                    },
                    "service_type": {
                        "type": "string",
                        "description": "Type of service for the appointment."
                    },
                    "preferred_date": {
                        "type": "string",
                        "format": "date",
                        "description": "Preferred date for the appointment (YYYY-MM-DD)."
                    },
                    "preferred_time": {
                        "type": "string",
                        "description": "Preferred time or time range (e.g., '14:00', 'morning')."
                    },
                    "provider_id": {
                        "type": "string",
                        "description": "Optional ID of a specific provider.",
                        "nullable": True
                    },
                },
                "required": ["service_type", "preferred_date", "preferred_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "reschedule_user_appointment",
            "description": "Reschedule an existing appointment to a new date or time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {
                        "type": "string",
                        "description": "The ID of the appointment to cancel. (This must pick from the appointment details, example id: 100, 101, or other numbers)",
                        "pattern": "^[0-9]{1,10}$"
                    },
                    "new_date": {
                        "type": "string",
                        "format": "date",
                        "description": "New date (YYYY-MM-DD)."
                    },
                    "new_time": {
                        "type": "string",
                        "description": "New time or time range."
                    }
                },
                "required": ["appointment_id", "new_date", "new_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_user_appointment",
            "description": "Cancel an upcoming or existing appointment for the current user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "appointment_id": {
                        "type": "string",
                        "description": "The ID of the appointment to cancel. (This must pick from the appointment details, example id: 100, 101, or other numbers)",
                        "pattern": "^[0-9]{1,10}$"
                    },
                },
                "required": ["appointment_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_available_slots",
            "description": "Get available time slots for booking a new appointment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_type": {
                        "type": "string",
                        "description": "Type of service (e.g. dental, eye check)."
                    },
                    "date": {
                        "type": "string",
                        "format": "date",
                        "description": "Preferred date to search slots for (YYYY-MM-DD)."
                    },
                    "provider_id": {
                        "type": "string",
                        "description": "Optional provider ID to check their availability.",
                        "nullable": True
                    }
                },
                "required": ["service_type", "date"],
            },
        },
    },
]
