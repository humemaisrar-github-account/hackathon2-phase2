/**
 * Test script to verify signup and login functionality works correctly
 */

const axios = require('axios');

async function testSignupAndLogin() {
  console.log('🧪 Testing signup and login functionality...\n');

  try {
    // Test data
    const email = `testuser_${Date.now()}@example.com`;
    const password = 'TestPassword123!';

    console.log('📝 Testing signup...');

    // First, try to register via BetterAuth (frontend)
    console.log('   → Calling BetterAuth signup endpoint (/api/auth/sign-up)');
    const betterAuthSignupResponse = await fetch('http://localhost:3000/api/auth/sign-up', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    console.log(`   ← BetterAuth signup response: ${betterAuthSignupResponse.status}`);

    if (!betterAuthSignupResponse.ok) {
      const errorText = await betterAuthSignupResponse.text();
      console.log(`   ❌ BetterAuth signup failed: ${errorText}`);
      return false;
    }

    const betterAuthSignupData = await betterAuthSignupResponse.json();
    console.log('   ✅ BetterAuth signup successful');

    // Now test login via BetterAuth (frontend)
    console.log('\n🔐 Testing login...');
    console.log('   → Calling BetterAuth login endpoint (/api/auth/sign-in)');

    const betterAuthLoginResponse = await fetch('http://localhost:3000/api/auth/sign-in', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    console.log(`   ← BetterAuth login response: ${betterAuthLoginResponse.status}`);

    if (!betterAuthLoginResponse.ok) {
      const errorText = await betterAuthLoginResponse.text();
      console.log(`   ❌ BetterAuth login failed: ${errorText}`);
      return false;
    }

    const betterAuthLoginData = await betterAuthLoginResponse.json();
    console.log('   ✅ BetterAuth login successful');

    // Now test the backend integration by getting a JWT token
    console.log('\n🔑 Testing backend JWT integration...');
    console.log('   → Calling backend login endpoint to get JWT token');

    const backendLoginResponse = await axios.post('http://localhost:8000/api/auth/login', {
      email: email,
      password: password,
    });

    console.log(`   ← Backend login response: ${backendLoginResponse.status}`);
    console.log('   ✅ Backend JWT token received');

    // Extract JWT token
    const jwtToken = backendLoginResponse.data.access_token;
    console.log(`   🪪 JWT token length: ${jwtToken ? jwtToken.length : 'N/A'}`);

    // Test creating a task with the JWT token
    console.log('\n📝 Testing task creation with JWT token...');
    console.log('   → Calling backend task creation endpoint');

    const taskResponse = await axios.post(
      `http://localhost:8000/api/${backendLoginResponse.data.user.id}/tasks`,
      {
        title: "Test task from signup/login test",
        description: "Created during signup/login functionality test"
      },
      {
        headers: {
          'Authorization': `Bearer ${jwtToken}`
        }
      }
    );

    console.log(`   ← Task creation response: ${taskResponse.status}`);
    console.log('   ✅ Task created successfully');

    console.log('\n🎉 All tests passed! Signup and login functionality working correctly.');
    return true;

  } catch (error) {
    console.error('\n💥 Test failed with error:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
    return false;
  }
}

// Run the test
testSignupAndLogin()
  .then(success => {
    console.log(`\n🏁 Test completed: ${success ? 'PASSED' : 'FAILED'}`);
    process.exit(success ? 0 : 1);
  })
  .catch(error => {
    console.error('Test script error:', error);
    process.exit(1);
  });