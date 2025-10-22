#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_URL="http://localhost:5001/api/v1"

echo "======================================"
echo "Testing HBnB Review Endpoints"
echo "======================================"

# Setup: Create user, place, and reviewer
echo -e "\n${YELLOW}Setup: Creating users and place${NC}"

# Use unique timestamp for emails
TIMESTAMP=$(date +%s)

# Create owner
OWNER_RESPONSE=$(curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -d "{\"first_name\": \"Alice\", \"last_name\": \"Owner\", \"email\": \"alice.review.$TIMESTAMP@example.com\"}")

# Debug: Show owner response
echo "Owner Response: $OWNER_RESPONSE"

# Parse owner ID with improved regex
OWNER_ID=$(echo "$OWNER_RESPONSE" | grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/' | head -1)
echo "Owner created with ID: $OWNER_ID"

# Verify owner ID is not empty
if [ -z "$OWNER_ID" ]; then
    echo -e "${RED}✗ Failed to create owner or parse ID${NC}"
    exit 1
fi

# Create reviewer
REVIEWER_RESPONSE=$(curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -d "{\"first_name\": \"Bob\", \"last_name\": \"Reviewer\", \"email\": \"bob.review.$TIMESTAMP@example.com\"}")

# Debug: Show reviewer response
echo "Reviewer Response: $REVIEWER_RESPONSE"

# Parse reviewer ID with improved regex
REVIEWER_ID=$(echo "$REVIEWER_RESPONSE" | grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/' | head -1)
echo "Reviewer created with ID: $REVIEWER_ID"

# Verify reviewer ID is not empty
if [ -z "$REVIEWER_ID" ]; then
    echo -e "${RED}✗ Failed to create reviewer or parse ID${NC}"
    exit 1
fi

# Create place
PLACE_RESPONSE=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Test Place for Reviews $TIMESTAMP\", \"description\": \"Test\", \"price\": 100.0, \"latitude\": 37.7749, \"longitude\": -122.4194, \"owner_id\": \"$OWNER_ID\"}")

# Debug: Show place response
echo "Place Response: $PLACE_RESPONSE"

# Parse place ID with improved regex
PLACE_ID=$(echo "$PLACE_RESPONSE" | grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/' | head -1)
echo "Place created with ID: $PLACE_ID"

# Verify place ID is not empty
if [ -z "$PLACE_ID" ]; then
    echo -e "${RED}✗ Failed to create place or parse ID${NC}"
    exit 1
fi

# Test 1: Create a new review
echo -e "\n${YELLOW}Test 1: Create a new review (POST)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/reviews/ \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Great place to stay!\", \"rating\": 5, \"user_id\": \"$REVIEWER_ID\", \"place_id\": \"$PLACE_ID\"}")
echo "Response: $RESPONSE"
REVIEW_ID=$(echo "$RESPONSE" | grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/' | head -1)
if [ ! -z "$REVIEW_ID" ]; then
  echo -e "${GREEN}✓ Review created with ID: $REVIEW_ID${NC}"
else
  echo -e "${RED}✗ Failed to create review${NC}"
fi

# Test 2: Get review by ID
echo -e "\n${YELLOW}Test 2: Get review by ID (GET)${NC}"
RESPONSE=$(curl -s -X GET $BASE_URL/reviews/$REVIEW_ID)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"$REVIEW_ID"* ]] && [[ $RESPONSE == *"Great place"* ]]; then
  echo -e "${GREEN}✓ Review retrieved successfully${NC}"
else
  echo -e "${RED}✗ Failed to retrieve review${NC}"
fi

# Test 3: Create another review
echo -e "\n${YELLOW}Test 3: Create another review${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/reviews/ \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Very comfortable and clean\", \"rating\": 4, \"user_id\": \"$REVIEWER_ID\", \"place_id\": \"$PLACE_ID\"}")
echo "Response: $RESPONSE"
REVIEW_ID_2=$(echo "$RESPONSE" | grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/' | head -1)
if [ ! -z "$REVIEW_ID_2" ]; then
  echo -e "${GREEN}✓ Second review created with ID: $REVIEW_ID_2${NC}"
else
  echo -e "${RED}✗ Failed to create second review${NC}"
fi

# Test 4: Get all reviews
echo -e "\n${YELLOW}Test 4: Get all reviews (GET)${NC}"
RESPONSE=$(curl -s -X GET $BASE_URL/reviews/)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"$REVIEW_ID"* ]] && [[ $RESPONSE == *"$REVIEW_ID_2"* ]]; then
  echo -e "${GREEN}✓ All reviews retrieved successfully${NC}"
else
  echo -e "${RED}✗ Failed to retrieve all reviews${NC}"
fi

# Test 5: Get reviews for a specific place
echo -e "\n${YELLOW}Test 5: Get reviews for a specific place (GET)${NC}"
RESPONSE=$(curl -s -X GET $BASE_URL/places/$PLACE_ID/reviews)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"$REVIEW_ID"* ]] && [[ $RESPONSE == *"$REVIEW_ID_2"* ]]; then
  echo -e "${GREEN}✓ Place reviews retrieved successfully${NC}"
else
  echo -e "${RED}✗ Failed to retrieve place reviews${NC}"
fi

# Test 6: Update review
echo -e "\n${YELLOW}Test 6: Update review (PUT)${NC}"
RESPONSE=$(curl -s -X PUT $BASE_URL/reviews/$REVIEW_ID \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Amazing place!\", \"rating\": 5, \"user_id\": \"$REVIEWER_ID\", \"place_id\": \"$PLACE_ID\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"Amazing place"* ]]; then
  echo -e "${GREEN}✓ Review updated successfully${NC}"
else
  echo -e "${RED}✗ Failed to update review${NC}"
fi

# Test 7: Invalid rating (out of range)
echo -e "\n${YELLOW}Test 7: Create review with invalid rating (should fail)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/reviews/ \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Test\", \"rating\": 6, \"user_id\": \"$REVIEWER_ID\", \"place_id\": \"$PLACE_ID\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Invalid rating correctly rejected${NC}"
else
  echo -e "${RED}✗ Should have rejected invalid rating${NC}"
fi

# Test 8: Non-existent user
echo -e "\n${YELLOW}Test 8: Create review with non-existent user (should fail)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/reviews/ \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Test\", \"rating\": 5, \"user_id\": \"fake-user-id\", \"place_id\": \"$PLACE_ID\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"not found"* ]] || [[ $RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Non-existent user correctly rejected${NC}"
else
  echo -e "${RED}✗ Should have rejected non-existent user${NC}"
fi

# Test 9: Non-existent place
echo -e "\n${YELLOW}Test 9: Create review for non-existent place (should fail)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/reviews/ \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Test\", \"rating\": 5, \"user_id\": \"$REVIEWER_ID\", \"place_id\": \"fake-place-id\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"not found"* ]] || [[ $RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Non-existent place correctly rejected${NC}"
else
  echo -e "${RED}✗ Should have rejected non-existent place${NC}"
fi

# Test 10: Delete review
echo -e "\n${YELLOW}Test 10: Delete review (DELETE)${NC}"
RESPONSE=$(curl -s -X DELETE $BASE_URL/reviews/$REVIEW_ID_2)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"deleted successfully"* ]]; then
  echo -e "${GREEN}✓ Review deleted successfully${NC}"
else
  echo -e "${RED}✗ Failed to delete review${NC}"
fi

# Test 11: Verify deletion
echo -e "\n${YELLOW}Test 11: Verify review was deleted (should return 404)${NC}"
RESPONSE=$(curl -s -X GET $BASE_URL/reviews/$REVIEW_ID_2)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"not found"* ]]; then
  echo -e "${GREEN}✓ Deleted review correctly not found${NC}"
else
  echo -e "${RED}✗ Review should have been deleted${NC}"
fi

# Test 12: Delete non-existent review
echo -e "\n${YELLOW}Test 12: Delete non-existent review (should return 404)${NC}"
RESPONSE=$(curl -s -X DELETE $BASE_URL/reviews/fake-review-id)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"not found"* ]]; then
  echo -e "${GREEN}✓ 404 correctly returned for delete${NC}"
else
  echo -e "${RED}✗ Should have returned 404${NC}"
fi

# Test 13: Get place with reviews
echo -e "\n${YELLOW}Test 13: Get place details with reviews included${NC}"
RESPONSE=$(curl -s -X GET $BASE_URL/places/$PLACE_ID)
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"reviews"* ]] && [[ $RESPONSE == *"$REVIEW_ID"* ]]; then
  echo -e "${GREEN}✓ Place details include reviews${NC}"
else
  echo -e "${RED}✗ Place should include reviews${NC}"
fi

# Test 14: Empty review text
echo -e "\n${YELLOW}Test 14: Create review with empty text (should fail)${NC}"
RESPONSE=$(curl -s -X POST $BASE_URL/reviews/ \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"\", \"rating\": 5, \"user_id\": \"$REVIEWER_ID\", \"place_id\": \"$PLACE_ID\"}")
echo "Response: $RESPONSE"
if [[ $RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Empty text correctly rejected${NC}"
else
  echo -e "${RED}✗ Should have rejected empty text${NC}"
fi

echo -e "\n======================================"
echo -e "${GREEN}All review tests completed!${NC}"
echo "======================================"