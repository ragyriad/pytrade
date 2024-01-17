import React, { useEffect,useState } from "react";
import { useDispatch,useSelector } from "react-redux";
import { Paper,Box } from "@mui/material";

import { setCommissionFilter } from "../Redux/slices/commissionSlice";
import { setAccountFilter } from "../Redux/slices/accountFilterSlice";

import MultipleSelectCheckmarks from "./SelectCheckmark";

const Account = ()  => {
    const dispatch = useDispatch()
    const [fetchedAccounts, setFetchedAccounts] = useState([])
    const [selectedAccounts, setSelectedAccounts] = useState([])
    const sentinels = [{"label": "commission"}, {"label":"desposits"}]

    const state = useSelector((state) => state)

    useEffect (() => {
        fetch('http://localhost:8000/api/account/get_all')
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            const accountData = data.accounts.map((account) => {
                return {"label": account.fields.type, "accountNumber": account.fields.accountNumber}
            })
            console.log("MODIFIED")
            console.log(accountData)
            setFetchedAccounts(accountData);
        })
    }, [])
 
    return (
        <div className="accountContainer" style={{
            width:"100%",
            display: "flex",
            justifyContent: "space-around"
            
        }}>
            {
                fetchedAccounts.map((accountObj,indx) => {
                    return (
                    <div style={{
                        width: "300px",
                        backgroundColor: "white",
                        display: "flex",
                        justifyContent: "center",
                        boxShadow: 'inset 0 3px 6px rgba(0,0,0,0.16), 0 4px 6px rgba(0,0,0,0.45)',
                        borderRadius: '10px'
                    }} key={accountObj.accountNumber + indx}>
                        <div>
                            <h2><button onClick={ () => {dispatch(setAccountFilter(accountObj.accountNumber));dispatch(setCommissionFilter(false))}}><a >{accountObj.label}</a></button></h2>
                        </div>
                    </div>)
                })
            }
            <div style={{
                        width: "300px",
                        backgroundColor: "white",
                        display: "flex",
                        justifyContent: "center",
                        boxShadow: 'inset 0 3px 6px rgba(0,0,0,0.16), 0 4px 6px rgba(0,0,0,0.45)',
                        borderRadius: '10px'
                    }}>
                <h2><button onClick={ () => {dispatch(setAccountFilter(0)); dispatch(setCommissionFilter(false));}}>All</button></h2>
            </div>
            <div style={{
                        width: "300px",
                        backgroundColor: "white",
                        display: "flex",
                        justifyContent: "center",
                        boxShadow: 'inset 0 3px 6px rgba(0,0,0,0.16), 0 4px 6px rgba(0,0,0,0.45)',
                        borderRadius: '10px'
                    }}>
                <h2><button onClick={ () => {dispatch(setCommissionFilter(true))}}>Commission Only</button></h2>
            </div>
            <Box>
                <Paper>
                    {fetchedAccounts.length > 0 ? <MultipleSelectCheckmarks data={fetchedAccounts}/> : <div></div>}
                    {sentinels.length > 0 ? <MultipleSelectCheckmarks data={sentinels}/> : <div></div>}
                </Paper>
            </Box>
        </div>
    )
}

export default Account