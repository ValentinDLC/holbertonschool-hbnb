#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_URL="http://localhost:5001/api/v1"

# Generate unique timestamp for emails
TIMESTAMP=$(date +%s)

echo "======================================"
echo "Testing HBnB Place Endpoints"
echo "======================================"

# Setup: Create a user (owner) and amenities first
echo -e "\n${YELLOW}Setup: Creating owner and amenities${NC}"

# Create owner with unique email
OWNER_RESPONSE=$(curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -d "{\"first_name\": \"John\", \"last_name\": \"Doe\", \"email\": \"john.place.${TIMESTAMP}@example.com\"}")
echo "Owner Response: $OWNER_RESPONSE"
OWNER_ID=$(echo "$OWNER_RESPONSE" | sed -n 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')

if [ -z "$OWNER_ID" ]; then
    OWNER_ID=$(echo "$OWNER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
fi

if [ -z "$OWNER_ID" ]; then
    echo -e "${RED}✗ Failed to create owner${NC}"
    exit 1
fi
echo -e "${GREEN}Owner created with ID: $OWNER_ID${NC}"

# Create WiFi amenity
WIFI_RESPONSE=$(curl -s -X POST $BASE_URL/amenities/ \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"WiFi for Places ${TIMESTAMP}\"}")
echo "WiFi Response: $WIFI_RESPONSE"
WIFI_ID=$(echo "$WIFI_RESPONSE" | sed -n 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')

if [ -z "$WIFI_ID" ]; then
    WIFI_ID=$(echo "$WIFI_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
fi

if [ -z "$WIFI_ID" ]; then
    echo -e "${RED}✗ Failed to create WiFi amenity${NC}"
    exit 1
fi
echo -e "${GREEN}WiFi amenity created with ID: $WIFI_ID${NC}"

# Create AC amenity
AC_RESPONSE=$(curl -s -X POST $BASE_URL/amenities/ \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Air Conditioning ${TIMESTAMP}\"}")
echo "AC Response: $AC_RESPONSE"
AC_ID=$(echo "$AC_RESPONSE" | sed -n 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')

if [ -z "$AC_ID" ]; then
    AC_ID=$(echo "$AC_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
fi

if [ -z "$AC_ID" ]; then
    echo -e "${RED}✗ Failed to create AC amenity${NC}"
    exit 1
fi
echo -e "${GREEN}AC amenity created with ID: $AC_ID${NC}"

# Test 1: Create a new place without amenities
echo -e "\n${YELLOW}Test 1: Create a new place without amenities (POST)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Cozy Apartment\", \"description\": \"A nice place to stay\", \"price\": 100.0, \"latitude\": 37.7749, \"longitude\": -122.4194, \"owner_id\": \"$OWNER_ID\"}")
echo "Response: $RESPONSE"

# Try Python first (most reliable for getting the top-level id)
PLACE_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)

# Fallback to jq if available
if [ -z "$PLACE_ID" ] && command -v jq &> /dev/null; then
    PLACE_ID=$(echo "$RESPONSE" | jq -r '.id' 2>/dev/null)
fi

# Last resort: sed
if [ -z "$PLACE_ID" ]; then
    PLACE_ID=$(echo "$RESPONSE" | sed -n 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
fi

if [ ! -z "$PLACE_ID" ]; then
  echo -e "${GREEN}✓ Place created with ID: $PLACE_ID${NC}"
else
  echo -e "${RED}✗ Failed to create place. Trying to extract ID from response...${NC}"
  # Debug: try to parse with grep differently
  PLACE_ID=$(echo "$RESPONSE" | grep -oP '"id"\s*:\s*"\K[^"]+' | head -1)
  if [ ! -z "$PLACE_ID" ]; then
    echo -e "${YELLOW}⚠ ID extracted with grep: $PLACE_ID${NC}"
  fi
fi

echo "DEBUG: PLACE_ID='$PLACE_ID'"

# Test 2: Create a place with amenities
echo -e "\n${YELLOW}Test 2: Create a place with amenities (POST)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Luxury Condo\", \"description\": \"Modern condo\", \"price\": 200.0, \"latitude\": 34.0522, \"longitude\": -118.2437, \"owner_id\": \"$OWNER_ID\", \"amenities\": [\"$WIFI_ID\", \"$AC_ID\"]}")
echo "Response: $RESPONSE"

# Try Python first (most reliable for getting the top-level id)
PLACE_ID_2=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)

# Fallback to jq if available
if [ -z "$PLACE_ID_2" ] && command -v jq &> /dev/null; then
    PLACE_ID_2=$(echo "$RESPONSE" | jq -r '.id' 2>/dev/null)
fi

# Last resort: sed
if [ -z "$PLACE_ID_2" ]; then
    PLACE_ID_2=$(echo "$RESPONSE" | sed -n 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)
fi

if [ ! -z "$PLACE_ID_2" ]; then
  echo -e "${GREEN}✓ Place with amenities created with ID: $PLACE_ID_2${NC}"
else
  echo -e "${RED}✗ Failed to create place with amenities. Trying to extract ID from response...${NC}"
  # Debug: try to parse with grep differently
  PLACE_ID_2=$(echo "$RESPONSE" | grep -oP '"id"\s*:\s*"\K[^"]+' | head -1)
  if [ ! -z "$PLACE_ID_2" ]; then
    echo -e "${YELLOW}⚠ ID extracted with grep: $PLACE_ID_2${NC}"
  fi
fi

echo "DEBUG: PLACE_ID_2='$PLACE_ID_2'"

# Test 3: Get place by ID
echo -e "\n${YELLOW}Test 3: Get place by ID (GET)${NC}"
RESPONSE=$(curl -s -X GET "$BASE_URL/places/$PLACE_ID_2")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"$PLACE_ID_2"* ]] && [[ $RESPONSE == *"owner"* ]] && [[ $RESPONSE == *"amenities"* ]]; then
  echo -e "${GREEN}✓ Place retrieved successfully with owner and amenities${NC}"
else
  echo -e "${RED}✗ Failed to retrieve place details${NC}"
fi

# Test 4: Get all places
echo -e "\n${YELLOW}Test 4: Get all places (GET)${NC}"
RESPONSE=$(curl -s -X GET $BASE_URL/places/)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"$PLACE_ID"* ]] && [[ $RESPONSE == *"$PLACE_ID_2"* ]]; then
  echo -e "${GREEN}✓ All places retrieved successfully${NC}"
else
  echo -e "${RED}✗ Failed to retrieve all places${NC}"
fi

# Test 5: Update place
echo -e "\n${YELLOW}Test 5: Update place (PUT)${NC}"
RESPONSE=$(curl -s -X PUT "$BASE_URL/places/$PLACE_ID" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Updated Apartment\", \"description\": \"An updated description\", \"price\": 150.0, \"latitude\": 37.7749, \"longitude\": -122.4194, \"owner_id\": \"$OWNER_ID\", \"amenities\": [\"$WIFI_ID\"]}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"Updated Apartment"* ]] && [[ $RESPONSE == *"150"* ]]; then
  echo -e "${GREEN}✓ Place updated successfully${NC}"
else
  echo -e "${RED}✗ Failed to update place${NC}"
fi

# Test 6: Invalid price (negative)
echo -e "\n${YELLOW}Test 6: Create place with negative price (should fail)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Test Place\", \"description\": \"Test\", \"price\": -50.0, \"latitude\": 0, \"longitude\": 0, \"owner_id\": \"$OWNER_ID\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Negative price correctly rejected${NC}"
else
  echo -e "${RED}✗ Should have rejected negative price${NC}"
fi

# Test 7: Invalid latitude
echo -e "\n${YELLOW}Test 7: Create place with invalid latitude (should fail)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Test Place\", \"description\": \"Test\", \"price\": 100.0, \"latitude\": 91, \"longitude\": 0, \"owner_id\": \"$OWNER_ID\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Invalid latitude correctly rejected${NC}"
else
  echo -e "${RED}✗ Should have rejected invalid latitude${NC}"
fi

# Test 8: Invalid longitude
echo -e "\n${YELLOW}Test 8: Create place with invalid longitude (should fail)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Test Place\", \"description\": \"Test\", \"price\": 100.0, \"latitude\": 0, \"longitude\": 181, \"owner_id\": \"$OWNER_ID\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Invalid longitude correctly rejected${NC}"
else
  echo -e "${RED}✗ Should have rejected invalid longitude${NC}"
fi

# Test 9: Non-existent owner
echo -e "\n${YELLOW}Test 9: Create place with non-existent owner (should fail)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Place", "description": "Test", "price": 100.0, "latitude": 0, "longitude": 0, "owner_id": "fake-owner-id"}')
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"Owner not found"* ]] || [[ $RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Non-existent owner correctly rejected${NC}"
else
  echo -e "${RED}✗ Should have rejected non-existent owner${NC}"
fi

# Test 10: Get non-existent place
echo -e "\n${YELLOW}Test 10: Get non-existent place (should return 404)${NC}"
RESPONSE=$(curl -s -X GET $BASE_URL/places/fake-place-id)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"not found"* ]]; then
  echo -e "${GREEN}✓ 404 correctly returned${NC}"
else
  echo -e "${RED}✗ Should have returned 404${NC}"
fi

# Test 11: Update non-existent place
echo -e "\n${YELLOW}Test 11: Update non-existent place (should return 404)${NC}"
RESPONSE=$(curl -s -X PUT $BASE_URL/places/fake-place-id \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Test\", \"description\": \"Test\", \"price\": 100.0, \"latitude\": 0, \"longitude\": 0, \"owner_id\": \"$OWNER_ID\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"not found"* ]]; then
  echo -e "${GREEN}✓ 404 correctly returned for update${NC}"
else
  echo -e "${RED}✗ Should have returned 404${NC}"
fi

# Test 12: Missing required fields
echo -e "\n${YELLOW}Test 12: Create place with missing title (should fail)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -d "{\"description\": \"Test\", \"price\": 100.0, \"latitude\": 0, \"longitude\": 0, \"owner_id\": \"$OWNER_ID\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"error"* ]] || [[ $RESPONSE == *"required"* ]]; then
  echo -e "${GREEN}✓ Missing title correctly rejected${NC}"
else
  echo -e "${RED}✗ Should have rejected missing title${NC}"
fi

echo -e "\n======================================"
echo -e "${GREEN}All place tests completed!${NC}"
echo "======================================"