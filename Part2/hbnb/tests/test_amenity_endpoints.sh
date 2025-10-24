#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_URL="http://localhost:5001/api/v1"

echo "======================================"
echo "Testing HBnB Amenity Endpoints"
echo "======================================"

# Clean up: Delete all existing amenities before running tests
echo -e "\n${YELLOW}Cleaning up existing amenities...${NC}"
EXISTING_AMENITIES=$(curl -s -X GET $BASE_URL/amenities/)
# Extract all IDs and delete them
IDS=$(echo "$EXISTING_AMENITIES" | grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/')
for ID in $IDS; do
    curl -s -X DELETE $BASE_URL/amenities/$ID > /dev/null 2>&1
done
echo -e "${GREEN}✓ Cleanup completed${NC}"

# Test 1: Create a new amenity
echo -e "\n${YELLOW}Test 1: Create a new amenity (POST)${NC}"
echo "Command: curl -X POST $BASE_URL/amenities/ -H 'Content-Type: application/json' -d '{\"name\": \"Wi-Fi\"}'"
RESPONSE=$(curl -s -X POST $BASE_URL/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}')
echo "Response: $RESPONSE"
# Fixed parsing to handle formatted JSON
AMENITY_ID=$(echo "$RESPONSE" | grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/' | head -1)
if [ ! -z "$AMENITY_ID" ]; then
  echo -e "${GREEN}✓ Amenity created with ID: $AMENITY_ID${NC}"
else
  echo -e "${RED}✗ Failed to create amenity${NC}"
fi

# Test 2: Get amenity by ID
echo -e "\n${YELLOW}Test 2: Get amenity by ID (GET)${NC}"
echo "Command: curl -X GET $BASE_URL/amenities/$AMENITY_ID"
RESPONSE=$(curl -s -X GET $BASE_URL/amenities/$AMENITY_ID)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"$AMENITY_ID"* ]] && [[ $RESPONSE == *"Wi-Fi"* ]]; then
  echo -e "${GREEN}✓ Amenity retrieved successfully${NC}"
else
  echo -e "${RED}✗ Failed to retrieve amenity${NC}"
fi

# Test 3: Create another amenity
echo -e "\n${YELLOW}Test 3: Create another amenity${NC}"
echo "Command: curl -X POST $BASE_URL/amenities/ -H 'Content-Type: application/json' -d '{\"name\": \"Air Conditioning\"}'"
RESPONSE=$(curl -s -X POST $BASE_URL/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Air Conditioning"}')
echo "Response: $RESPONSE"
# Fixed parsing to handle formatted JSON
AMENITY_ID_2=$(echo "$RESPONSE" | grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/' | head -1)
if [ ! -z "$AMENITY_ID_2" ]; then
  echo -e "${GREEN}✓ Second amenity created with ID: $AMENITY_ID_2${NC}"
else
  echo -e "${RED}✗ Failed to create second amenity${NC}"
fi

# Test 4: Get all amenities
echo -e "\n${YELLOW}Test 4: Get all amenities (GET)${NC}"
echo "Command: curl -X GET $BASE_URL/amenities/"
RESPONSE=$(curl -s -X GET $BASE_URL/amenities/)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"$AMENITY_ID"* ]] && [[ $RESPONSE == *"$AMENITY_ID_2"* ]]; then
  echo -e "${GREEN}✓ All amenities retrieved successfully${NC}"
else
  echo -e "${RED}✗ Failed to retrieve all amenities${NC}"
fi

# Test 5: Update amenity
echo -e "\n${YELLOW}Test 5: Update amenity (PUT)${NC}"
echo "Command: curl -X PUT $BASE_URL/amenities/$AMENITY_ID -H 'Content-Type: application/json' -d '{\"name\": \"Free Wi-Fi\"}'"
RESPONSE=$(curl -s -X PUT $BASE_URL/amenities/$AMENITY_ID \
  -H "Content-Type: application/json" \
  -d '{"name": "Free Wi-Fi"}')
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"Free Wi-Fi"* ]]; then
  echo -e "${GREEN}✓ Amenity updated successfully${NC}"
else
  echo -e "${RED}✗ Failed to update amenity${NC}"
fi

# Test 6: Try to create duplicate amenity
echo -e "\n${YELLOW}Test 6: Try to create duplicate amenity (should fail)${NC}"
echo "Command: curl -X POST $BASE_URL/amenities/ -H 'Content-Type: application/json' -d '{\"name\": \"Free Wi-Fi\"}'"
RESPONSE=$(curl -s -X POST $BASE_URL/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Free Wi-Fi"}')
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"already exists"* ]]; then
  echo -e "${GREEN}✓ Duplicate amenity correctly rejected${NC}"
else
  echo -e "${RED}✗ Should have rejected duplicate amenity${NC}"
fi

# Test 7: Get non-existent amenity
echo -e "\n${YELLOW}Test 7: Get non-existent amenity (should return 404)${NC}"
echo "Command: curl -X GET $BASE_URL/amenities/fake-id-123"
RESPONSE=$(curl -s -X GET $BASE_URL/amenities/fake-id-123)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"not found"* ]]; then
  echo -e "${GREEN}✓ 404 correctly returned${NC}"
else
  echo -e "${RED}✗ Should have returned 404${NC}"
fi

# Test 8: Update non-existent amenity
echo -e "\n${YELLOW}Test 8: Update non-existent amenity (should return 404)${NC}"
echo "Command: curl -X PUT $BASE_URL/amenities/fake-id-123 -H 'Content-Type: application/json' -d '{\"name\": \"Test\"}'"
RESPONSE=$(curl -s -X PUT $BASE_URL/amenities/fake-id-123 \
  -H "Content-Type: application/json" \
  -d '{"name": "Test"}')
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"not found"* ]]; then
  echo -e "${GREEN}✓ 404 correctly returned for update${NC}"
else
  echo -e "${RED}✗ Should have returned 404${NC}"
fi

# Test 9: Create amenity with empty name
echo -e "\n${YELLOW}Test 9: Create amenity with empty name (should fail)${NC}"
echo "Command: curl -X POST $BASE_URL/amenities/ -H 'Content-Type: application/json' -d '{\"name\": \"\"}'"
RESPONSE=$(curl -s -X POST $BASE_URL/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": ""}')
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Empty name correctly rejected${NC}"
else
  echo -e "${RED}✗ Should have rejected empty name${NC}"
fi

# Test 10: Create amenity with name too long
echo -e "\n${YELLOW}Test 10: Create amenity with name too long (should fail)${NC}"
LONG_NAME="This is a very long amenity name that exceeds the maximum allowed length of fifty characters"
echo "Command: curl -X POST $BASE_URL/amenities/ -H 'Content-Type: application/json' -d '{\"name\": \"$LONG_NAME\"}'"
RESPONSE=$(curl -s -X POST $BASE_URL/amenities/ \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"$LONG_NAME\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Long name correctly rejected${NC}"
else
  echo -e "${RED}✗ Should have rejected long name${NC}"
fi

echo -e "\n======================================"
echo -e "${GREEN}All amenity tests completed!${NC}"
echo "======================================"