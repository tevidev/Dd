def format_result(result: dict, gate: str, bin_info: dict):
    status = result.get("status", "").upper()
    message = result.get("message", "Unknown")
    cc = result.get("cc", "N/A")

    if status == "LIVE":
        title = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
        status_line = f"Approved ✅ {message}"
    else:
        title = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
        status_line = f"Declined ❌ {message}"

    if not bin_info:
        bin_block = (
            "[ϟ] 𝗕𝗶𝗻 : N/A\n"
            "[ϟ] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 : N/A\n"
            "[ϟ] 𝗜𝘀𝘀𝘂𝗲𝗿 : N/A\n"
            "[ϟ] 𝗧𝘆𝗽𝗲 : N/A"
        )
    else:
        bin_block = (
            f"[ϟ] 𝗕𝗶𝗻 : {cc[:6]}\n"
            f"[ϟ] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 : {bin_info['country']} {bin_info['emoji']}\n"
            f"[ϟ] 𝗜𝘀𝘀𝘂𝗲𝗿 : {bin_info['bank']}\n"
            f"[ϟ] 𝗧𝘆𝗽𝗲 : {bin_info['scheme']} | {bin_info['type']} - {bin_info['brand']}"
        )

    return (
        f"{title}\n"
        f"━━━━━━━━━━━━━\n"
        f"[ϟ] 𝗖𝗖 - {cc}\n"
        f"[ϟ] 𝗦𝘁𝗮𝘁𝘂𝘀 : {status_line}\n"
        f"[ϟ] 𝗚𝗮𝘁𝗲 - {gate.upper()} 🧠\n"
        f"━━━━━━━━━━━━━\n"
        f"{bin_block}"
    )
