# %% import guardrails from hub
# !guardrails hub install hub://guardrails/detect_pii # pii detector
# !guardrails hub install hub://guardrails/toxic_language # toxic language detector
# !guardrails hub install hub://guardrails/competitor_check # competitor check

# %% module imports
from guardrails import Guard, OnFailAction
from guardrails.hub import DetectPII, ToxicLanguage, CompetitorCheck

# %% define the email pattern and a pii guard
guard = Guard().use(DetectPII, ["EMAIL_ADDRESS"], on_fail=OnFailAction.EXCEPTION)

# %% test with a string containing an email
input_text = "My email is xxx@domain.com"

try:
    guard.validate(input_text)
except Exception as e:
    print(e)

# %%  test with a string containing an email and a profanity
input_text = "My email is xxx@domain.com and I hate you since you work for Comapany Z"

guards = Guard().use_many(
    CompetitorCheck(["Company Z"], on_fail=OnFailAction.EXCEPTION),
    ToxicLanguage(
        threshold=0.5, validation_method="sentence", on_fail=OnFailAction.EXCEPTION
    ),
    DetectPII(["EMAIL_ADDRESS"], on_fail=OnFailAction.EXCEPTION),
)

try:
    guards.validate(input_text)
except Exception as e:
    print(e)

# %%
