# def mask_inner(plain, keep_start: int, keep_end: int, mask_char: str = "*"):
#     if len(plain) <= keep_start + keep_end:
#         return plain
#     else:
#         masked_chars = len(plain) - keep_start - keep_end
#         masked = plain[:keep_start] + mask_char * masked_chars
#         if keep_end > 0:
#             masked += plain[-keep_end:]
#         return masked


# def mask_email(email: str) -> str:
#     username, domain = email.split("@")
#     masked_username = username[0] + "*" * (len(username) - 2) + username[-1]
#     return masked_username + "@" + domain


# def mask_phone_number(phone_number: str) -> str:
#     return mask_inner(phone_number, keep_start=2, keep_end=3)


# def mask_common(plain: str) -> str:
#     return mask_inner(plain, keep_start=3, keep_end=0)
