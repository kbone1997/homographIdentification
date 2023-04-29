
        // Import the functions you need from the SDKs you need
        import { initializeApp } from "https://www.gstatic.com/firebasejs/9.8.1/firebase-app.js";
        import { getDatabase,ref,update } from "https://www.gstatic.com/firebasejs/9.8.1/firebase-database.js";
        import { getAuth,signInWithEmailAndPassword,onAuthStateChanged ,signOut  } from "https://www.gstatic.com/firebasejs/9.8.1/firebase-auth.js";
        // TODO: Add SDKs for Firebase products that you want to use
        // https://firebase.google.com/docs/web/setup#available-libraries
      
        // Your web app's Firebase configuration
        const firebaseConfig = {
          apiKey: "AIzaSyB5xmG6SoP5fzGNkkjm3SABZ2vgMG0R-pc",
          authDomain: "ewalletauth.firebaseapp.com",
          databaseURL: "https://ewalletauth-default-rtdb.firebaseio.com",
          projectId: "ewalletauth",
          storageBucket: "ewalletauth.appspot.com",
          messagingSenderId: "885575894639",
          appId: "1:885575894639:web:6e29d1e95d7e96c0c3af9a"
        };
      
        // Initialize Firebase
        const app = initializeApp(firebaseConfig);
        const database = getDatabase(app);
        const  auth = getAuth();

          const Login = document.querySelector('#Login');
              Login.addEventListener('click',(e)=>{

                     const email= document.getElementById('email').value;
                    const password = document.getElementById('password').value;
                    const phoneNumber = document.getElementById('phoneNumber').value;
                    
                    signInWithEmailAndPassword(auth, email, password)
                    .then((userCredential) => {
                    // Signed in 
                      const user = userCredential.user;
                      alert('logged In');
                      const date = new Date();

                    update(ref(database,'users/'+user.uid),{
                      last_login: date
                    })
                    
                      // ...
                      })
                      .catch((error) => {
                      const errorCode = error.code;
                      const errorMessage = error.message;
                      alert(errorMessage+'here occured'+'here occured 2');
                      });
                      //window.open("../indexSignIn.html","_self");
                      redirectToUser()
                    })
                    function redirectToUser(){
                      console.log("user fired")
                      window.open("index.html");
                    }
    
              const user = auth.currentUser;
              onAuthStateChanged(auth, (user) => {
                console.log(user)
                if (user) {
                  // User is signed in, see docs for a list of available properties
                  // https://firebase.google.com/docs/reference/js/firebase.User
                  const uid = user.email;
                  alert(uid)
                  // ...
                } else {
                  // User is signed out
                  // ...
                }
              });


              const balance = ref(database,'users/'+user.uid);
              onValue(balance,(snapshot)=>{
                const data = snapshot.val();
                console.log(data);
              })

              