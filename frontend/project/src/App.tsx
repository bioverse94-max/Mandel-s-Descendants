import { useState } from "react";
import HomePage from "./components/HomePage";
import LoadingScreen from "./components/LoadingScreen";

function App() {
  
  const [loadingComplete, setLoadingComplete] = useState(false);

  return (
    <div>
      {!loadingComplete ? (
        <LoadingScreen onComplete={() => setLoadingComplete(true)} />
      ) : (
        <HomePage />
      )}

    </div>
  );
}

export default App;
