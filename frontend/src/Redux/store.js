import { configureStore } from '@reduxjs/toolkit'
import setCommissionFilterReducer from "./slices/commissionSlice";
import setAccountFilterReducer from "./slices/accountFilterSlice";

const store = configureStore({
    reducer: {
        commissionFilter: setCommissionFilterReducer,
        accountFilter: setAccountFilterReducer
    }
});

export default store;