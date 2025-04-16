{
    **schema_registry.get("question_base"),
    "séquence": {
        "required": True,
        "type": "list",
        "empty": False,
        "valuesrules": {"type": "string"},
    },
}
