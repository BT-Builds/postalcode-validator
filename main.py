from fastapi import FastAPI, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import re

app = FastAPI(title="Postal Code Validator API", version="1.0.0")
# === BT Builds Standard Middleware (auto-injected) ===
from fastapi.middleware.cors import CORSMiddleware as _BTCors
app.add_middleware(_BTCors, allow_origins=["*"], allow_methods=["*"],
    allow_headers=["*"], expose_headers=["X-RateLimit-Limit","X-RateLimit-Remaining","X-RateLimit-Reset"])

@app.middleware("http")
async def _bt_add_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Powered-By"] = "btbuilds"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


security = HTTPBearer(auto_error=False)

API_KEY = "demo-key-change-in-production"

# Postal code regex patterns by country
POSTAL_PATTERNS = {
    "US": r"^\d{5}(-\d{4})?$",
    "CA": r"^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$",
    "GB": r"^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$",
    "DE": r"^\d{5}$",
    "FR": r"^\d{5}$",
    "IT": r"^\d{5}$",
    "ES": r"^\d{5}$",
    "NL": r"^\d{4}[ ]?[A-Z]{2}$",
    "BE": r"^\d{4}$",
    "AU": r"^\d{4}$",
    "JP": r"^\d{3}-?\d{4}$",
    "IN": r"^\d{6}$",
    "BR": r"^\d{5}-?\d{3}$",
    "MX": r"^\d{5}$",
    "RU": r"^\d{6}$",
    "CN": r"^\d{6}$",
    "KR": r"^\d{5}$",
    "PT": r"^\d{4}-?\d{3}$",
    "IE": r"^[AC-FHKNPRTV-Y]\d{2}$|^[AC-FHKNPRTV-Y]\d{3}[AC-FHKNPRTV-Y]{2}$",
    "AT": r"^\d{4}$",
}

class PostalCodeRequest(BaseModel):
    postal_code: str
    country_code: str

class PostalCodeResponse(BaseModel):
    postal_code: str
    country_code: str
    valid: bool
    formatted: str

def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials and credentials.credentials == API_KEY:
        return credentials.credentials
    raise HTTPException(status_code=401, detail="Invalid or missing API key")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/validate")
def validate_postalcode(request: PostalCodeRequest, api_key: str = Security(get_api_key)):
    code = request.postal_code.upper().strip()
    country = request.country_code.upper().strip()
    
    if country not in POSTAL_PATTERNS:
        raise HTTPException(status_code=400, detail=f"Unsupported country code: {country}")
    
    pattern = POSTAL_PATTERNS[country]
    is_valid = bool(re.match(pattern, code))
    
    formatted = code
    if country == "NL":
        formatted = code.replace(" ", "")[:4] + " " + code.replace(" ", "")[4:] if len(code.replace(" ", "")) == 6 else code
    elif country == "UK":
        formatted = code.upper()
    
    return PostalCodeResponse(
        postal_code=request.postal_code,
        country_code=country,
        valid=is_valid,
        formatted=formatted
    )

@app.get("/countries")
def list_countries():
    return {"countries": list(POSTAL_PATTERNS.keys())}

@app.get("/")
def read_root():
    return {"service": "Postal Code Validator API", "docs": "/docs"}

try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except ImportError:
    pass
