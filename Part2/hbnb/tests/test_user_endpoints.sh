#!/bin/bash
# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'
BASE_URL="http://localhost:5001/api/v1"

echo "======================================"
echo "Testing HBnB User Endpoints"
echo "======================================"

# Generate unique email using timestamp
TIMESTAMP=$(date +%s)
UNIQUE_EMAIL="john.doe.${TIMESTAMP}@example.com"
UPDATED_EMAIL="jane.doe.${TIMESTAMP}@example.com"

echo "Using unique email: $UNIQUE_EMAIL"

# Test 1: Create a new user
echo -e "\n${YELLOW}Test 1: Create a new user (POST)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/users/ \
-H "Content-Type: application/json" \
-d "{\"first_name\": \"John\", \"last_name\": \"Doe\", \"email\": \"$UNIQUE_EMAIL\"}")
echo "Response: $RESPONSE"

# Extract USER_ID - using sed which works on all systems
USER_ID=$(echo "$RESPONSE" | sed -n 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')

if [ -z "$USER_ID" ]; then
    echo -e "${RED}✗ Failed to create user or extract ID${NC}"
    echo "Trying alternative extraction method..."
    # Fallback to python if sed fails
    USER_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
fi

if [ -z "$USER_ID" ]; then
    echo -e "${RED}✗ Still failed to extract ID${NC}"
    exit 1
fi

echo -e "${GREEN}✓ User created with ID: $USER_ID${NC}"

# Test 2: Get user by ID
echo -e "\n${YELLOW}Test 2: Get user by ID (GET)${NC}"
RESPONSE=$(curl -s -X GET "$BASE_URL/users/$USER_ID")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"$USER_ID"* ]] && [[ $RESPONSE == *"John"* ]]; then
    echo -e "${GREEN}✓ User retrieved successfully${NC}"
else
    echo -e "${RED}✗ Failed to retrieve user${NC}"
fi

# Test 3: Get all users
echo -e "\n${YELLOW}Test 3: Get all users (GET)${NC}"
RESPONSE=$(curl -s -X GET $BASE_URL/users/)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"$USER_ID"* ]]; then
    echo -e "${GREEN}✓ All users retrieved successfully${NC}"
else
    echo -e "${RED}✗ Failed to retrieve all users${NC}"
fi

# Test 4: Update user
echo -e "\n${YELLOW}Test 4: Update user (PUT)${NC}"
RESPONSE=$(curl -s -X PUT "$BASE_URL/users/$USER_ID" \
-H "Content-Type: application/json" \
-d "{\"first_name\": \"Jane\", \"last_name\": \"Doe\", \"email\": \"$UPDATED_EMAIL\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"Jane"* ]] && [[ $RESPONSE == *"$UPDATED_EMAIL"* ]]; then
    echo -e "${GREEN}✓ User updated successfully${NC}"
else
    echo -e "${RED}✗ Failed to update user${NC}"
    echo "Expected to find 'Jane' and '$UPDATED_EMAIL' in response"
fi

# Test 5: Duplicate email
echo -e "\n${YELLOW}Test 5: Try duplicate email (should fail)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/users/ \
-H "Content-Type: application/json" \
-d "{\"first_name\": \"Test\", \"last_name\": \"User\", \"email\": \"$UPDATED_EMAIL\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"Email already registered"* ]]; then
    echo -e "${GREEN}✓ Duplicate email correctly rejected${NC}"
else
    echo -e "${RED}✗ Should have rejected duplicate email${NC}"
fi

# Test 6: User not found
echo -e "\n${YELLOW}Test 6: Get non-existent user (should return 404)${NC}"
RESPONSE=$(curl -s -X GET $BASE_URL/users/fake-id-123)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"User not found"* ]]; then
    echo -e "${GREEN}✓ 404 correctly returned${NC}"
else
    echo -e "${RED}✗ Should have returned 404${NC}"
fi

echo -e "\n======================================"
echo -e "${GREEN}All tests completed!${NC}"
echo "======================================"