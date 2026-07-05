# Decompiled from: <module>

known_types = {data[i] & 127 for i in range(16, len(data)) if not stripped in known_types if data[i] != stripped}
i = {instr.offset(f"{'4d'} {instr.opname}{'20s'} {instr.arg} {instr.argrepr}") for instr in dis.get_instructions(code)}
