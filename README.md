# Postal Code Validator API

Validate postal codes for 19 countries using regex patterns.

## Endpoints

### POST /validate
Validate a postal code against country format rules.

**Headers:**
```
Authorization: Bearer demo-key-change-in-production
Content-Type: application/json
```

**Body:**
```json
{
  "postal_code": "12345",
  "country_code": "US"
}
```

**Response:**
```json
{
  "postal_code": "12345",
  "country_code": "US",
  "valid": true,
  "formatted": "12345"
}
```

### GET /countries
List supported country codes.

**Response:**
```json
{
  "countries": ["US", "CA", "GB", "DE", "FR", "IT", "ES", "NL", "BE", "AU", "JP", "IN", "BR", "MX", "RU", "CN", "KR", "PT", "IE", "AT"]
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## Example Usage

```bash
curl -X POST https://postalcode-validator.vercel.app/validate \
  -H "Authorization: Bearer demo-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{"postal_code": "90210", "country_code": "US"}'
```

```bash
curl -X POST https://postalcode-validator.vercel.app/validate \
  -H "Authorization: Bearer demo-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{"postal_code": "K1A 0B1", "country_code": "CA"}'
```

## Supported Countries
US, CA, GB, DE, FR, IT, ES, NL, BE, AU, JP, IN, BR, MX, RU, CN, KR, PT, IE, AT