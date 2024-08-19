import LandingPage from "./Pages/LandingPage";
import AuthWrapper from "./Services/AuthWrapper";

import React from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import store from "../Redux/store";
import { PersistGate } from "redux-persist/integration/react";
import { persistStore } from "redux-persist";

const App = () => {
  let persistedStore = persistStore(store);
  return (
    <React.StrictMode>
      <Provider store={store}>
        <PersistGate persistor={persistedStore}>
          <AuthWrapper>
            <LandingPage />
          </AuthWrapper>
        </PersistGate>
      </Provider>
    </React.StrictMode>
  );
};

const root = createRoot(document.getElementById("app"));
root.render(<App />);
export default App;
