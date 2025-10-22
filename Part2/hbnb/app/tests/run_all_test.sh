#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================"
echo "HBnB API - Complete Test Suite"
echo "======================================${NC}"
echo ""

# Check if Flask app is running
echo -e "${YELLOW}Checking if Flask app is running...${NC}"
if curl -s http://localhost:5001/api/v1/ > /dev/null; then
    echo -e "${GREEN}✓ Flask app is running${NC}"
else
    echo -e "${RED}✗ Flask app is not running${NC}"
    echo "Please start the Flask app first: python run.py"
    exit 1
fi

echo ""
echo -e "${BLUE}======================================"
echo "Running Manual Tests (cURL)"
echo "======================================${NC}"

# Run all bash test scripts
test_files=(
    "tests/test_user_endpoints.sh"
    "tests/test_amenity_endpoints.sh"
    "tests/test_place_endpoints.sh"
    "tests/test_review_endpoints.sh"
)

manual_tests_passed=0
manual_tests_total=0

for test_file in "${test_files[@]}"; do
    if [ -f "$test_file" ]; then
        echo ""
        echo -e "${YELLOW}Running: $test_file${NC}"
        chmod +x "$test_file"
        if ./"$test_file" | tee /tmp/test_output.log; then
            # Count passed and total tests from output
            passed=$(grep -o "✓" /tmp/test_output.log | wc -l)
            total=$(grep -E "✓|✗" /tmp/test_output.log | wc -l)
            manual_tests_passed=$((manual_tests_passed + passed))
            manual_tests_total=$((manual_tests_total + total))
            echo -e "${GREEN}Completed: $test_file${NC}"
        else
            echo -e "${RED}Failed: $test_file${NC}"
        fi
    else
        echo -e "${RED}Test file not found: $test_file${NC}"
    fi
done

echo ""
echo -e "${BLUE}======================================"
echo "Running Automated Unit Tests"
echo "======================================${NC}"

# Run Python unit tests
if [ -f "tests/test_endpoints.py" ]; then
    echo -e "${YELLOW}Running: tests/test_endpoints.py${NC}"
    python3 -m unittest tests.test_endpoints -v 2>&1 | tee /tmp/unittest_output.log
    
    # Extract test results
    if grep -q "OK" /tmp/unittest_output.log; then
        unit_tests_result="PASSED"
        unit_tests_color=$GREEN
    else
        unit_tests_result="FAILED"
        unit_tests_color=$RED
    fi
    
    # Count tests
    unit_tests_run=$(grep -oP "Ran \K\d+" /tmp/unittest_output.log || echo "0")
    
    echo ""
    echo -e "${unit_tests_color}Unit Tests: $unit_tests_result${NC}"
    echo -e "Tests run: $unit_tests_run"
else
    echo -e "${RED}Unit test file not found: tests/test_endpoints.py${NC}"
    unit_tests_result="NOT FOUND"
    unit_tests_run=0
fi

echo ""
echo -e "${BLUE}======================================"
echo "Running Facade Tests"
echo "======================================${NC}"

# Run facade tests if they exist
if [ -f "tests/test_facade.py" ]; then
    echo -e "${YELLOW}Running: tests/test_facade.py${NC}"
    python3 tests/test_facade.py 2>&1 | tee /tmp/facade_output.log
    
    if grep -q "All Facade tests passed" /tmp/facade_output.log; then
        facade_result="PASSED"
        facade_color=$GREEN
    else
        facade_result="FAILED"
        facade_color=$RED
    fi
    
    echo ""
    echo -e "${facade_color}Facade Tests: $facade_result${NC}"
else
    echo -e "${YELLOW}Facade test file not found (optional)${NC}"
    facade_result="N/A"
fi

echo ""
echo -e "${BLUE}======================================"
echo "Test Summary"
echo "======================================${NC}"
echo ""
echo -e "${YELLOW}Manual Tests (cURL):${NC}"
echo -e "  Passed: ${GREEN}$manual_tests_passed${NC} / $manual_tests_total"
echo ""
echo -e "${YELLOW}Automated Unit Tests:${NC}"
echo -e "  Status: ${unit_tests_color}$unit_tests_result${NC}"
echo -e "  Tests run: $unit_tests_run"
echo ""
echo -e "${YELLOW}Facade Tests:${NC}"
echo -e "  Status: ${facade_color}$facade_result${NC}"
echo ""

# Calculate overall success
if [ "$unit_tests_result" = "PASSED" ] && [ $manual_tests_total -gt 0 ]; then
    overall_percentage=$((manual_tests_passed * 100 / manual_tests_total))
    echo -e "${YELLOW}Overall Success Rate:${NC} ${GREEN}$overall_percentage%${NC}"
    
    if [ $manual_tests_passed -eq $manual_tests_total ] && [ "$unit_tests_result" = "PASSED" ]; then
        echo ""
        echo -e "${GREEN}╔════════════════════════════════╗${NC}"
        echo -e "${GREEN}║  ALL TESTS PASSED! ✓✓✓        ║${NC}"
        echo -e "${GREEN}╚════════════════════════════════╝${NC}"
        exit 0
    else
        echo ""
        echo -e "${YELLOW}Some tests did not pass. Please review the output above.${NC}"
        exit 1
    fi
else
    echo ""
    echo -e "${RED}Tests incomplete or failed. Please review the output above.${NC}"
    exit 1
fi