/**
 * Simple test to verify the Todo API endpoints work correctly
 */

// Mock test data
const testData = {
  email: "test@example.com",
  password: "TestPass123!",
  userId: null,
  taskId: null
};

async function runTests() {
  console.log("Starting Todo API tests...\n");

  try {
    // Test 1: Sign up
    console.log("1. Testing sign up...");
    const signUpResponse = await fetch('/api/auth/sign-up', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: testData.email,
        password: testData.password,
      }),
    });

    if (signUpResponse.ok) {
      const signUpData = await signUpResponse.json();
      console.log("✓ Sign up successful");

      // Get JWT token from backend
      const backendAuthResponse = await fetch('http://127.0.0.1:8000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: testData.email,
          password: testData.password,
        }),
      });

      let jwtToken = null;
      if (backendAuthResponse.ok) {
        const backendData = await backendAuthResponse.json();
        jwtToken = backendData.access_token;
        testData.userId = backendData.user.id;
        console.log("✓ JWT token obtained");
      }
    } else {
      console.log("✗ Sign up failed:", await signUpResponse.text());
      return;
    }

    // Wait a moment for the user to be fully registered
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Test 2: Create a task
    console.log("\n2. Testing create task...");
    if (jwtToken && testData.userId) {
      const createResponse = await fetch(`http://127.0.0.1:8000/api/${testData.userId}/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${jwtToken}`
        },
        body: JSON.stringify({
          title: "Test Task",
          description: "This is a test task"
        }),
      });

      if (createResponse.ok) {
        const createData = await createResponse.json();
        testData.taskId = createData.task.id;
        console.log("✓ Task created successfully:", createData.task.title);
      } else {
        console.log("✗ Task creation failed:", await createResponse.text());
      }
    } else {
      console.log("✗ Skipping task creation - no JWT token or user ID");
    }

    // Test 3: Get all tasks
    console.log("\n3. Testing get all tasks...");
    if (jwtToken && testData.userId) {
      const getResponse = await fetch(`http://127.0.0.1:8000/api/${testData.userId}/tasks`, {
        headers: {
          'Authorization': `Bearer ${jwtToken}`
        }
      });

      if (getResponse.ok) {
        const getData = await getResponse.json();
        console.log(`✓ Retrieved ${getData.tasks.length} tasks`);
      } else {
        console.log("✗ Get tasks failed:", await getResponse.text());
      }
    } else {
      console.log("✗ Skipping get tasks - no JWT token or user ID");
    }

    // Test 4: Update task
    console.log("\n4. Testing update task...");
    if (jwtToken && testData.userId && testData.taskId) {
      const updateResponse = await fetch(`http://127.0.0.1:8000/api/${testData.userId}/tasks/${testData.taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${jwtToken}`
        },
        body: JSON.stringify({
          title: "Updated Test Task",
          description: "This is an updated test task"
        }),
      });

      if (updateResponse.ok) {
        const updateData = await updateResponse.json();
        console.log("✓ Task updated successfully:", updateData.task.title);
      } else {
        console.log("✗ Task update failed:", await updateResponse.text());
      }
    } else {
      console.log("✗ Skipping task update - missing required data");
    }

    // Test 5: Toggle completion
    console.log("\n5. Testing toggle completion...");
    if (jwtToken && testData.userId && testData.taskId) {
      const toggleResponse = await fetch(`http://127.0.0.1:8000/api/${testData.userId}/tasks/${testData.taskId}/complete`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${jwtToken}`
        }
      });

      if (toggleResponse.ok) {
        const toggleData = await toggleResponse.json();
        console.log("✓ Task completion toggled:", toggleData.task.is_completed);
      } else {
        console.log("✗ Toggle completion failed:", await toggleResponse.text());
      }
    } else {
      console.log("✗ Skipping toggle completion - missing required data");
    }

    // Test 6: Delete task
    console.log("\n6. Testing delete task...");
    if (jwtToken && testData.userId && testData.taskId) {
      const deleteResponse = await fetch(`http://127.0.0.1:8000/api/${testData.userId}/tasks/${testData.taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${jwtToken}`
        }
      });

      if (deleteResponse.ok) {
        const deleteData = await deleteResponse.json();
        console.log("✓ Task deleted successfully");
      } else {
        console.log("✗ Task deletion failed:", await deleteResponse.text());
      }
    } else {
      console.log("✗ Skipping task deletion - missing required data");
    }

    console.log("\n✓ All tests completed!");
  } catch (error) {
    console.error("✗ Test execution error:", error.message);
  }
}

// Run tests if this file is executed directly
if (typeof window !== 'undefined') {
  // Browser environment
  runTests().catch(console.error);
} else {
  // Node.js environment
  // This would need to be adapted for server-side execution
}