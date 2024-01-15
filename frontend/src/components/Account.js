import React, { useEffect,useState } from "react";
import { useDispatch } from "react-redux";
import { setCommissionFilter } from "../Redux/slices/commissionSlice";
import { setAccountFilter } from "../Redux/slices/accountFilterSlice";

const Account = ()  => {
    const dispatch = useDispatch()
    const [accounts, setAccounts] = useState([])

    useEffect (() => {
        fetch('http://localhost:8000/api/account/get_all')
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            setAccounts(data.accounts);
        })
    }, [])
 
    return (
        <div className="accountContainer" style={{
            width:"100%",
            display: "flex",
            justifyContent: "space-around"
            
        }}>
            {
                accounts.map((accountObj,indx) => {
                    return (
                    <div style={{
                        width: "300px",
                        backgroundColor: "white",
                        display: "flex",
                        justifyContent: "center",
                        boxShadow: 'inset 0 3px 6px rgba(0,0,0,0.16), 0 4px 6px rgba(0,0,0,0.45)',
                        borderRadius: '10px'
                    }} key={accountObj.fields.accountNumber + indx}>
                        {console.log(accountObj.fields.accountNumber)}
                        <div>
                            <h2><button onClick={ () => {dispatch(setAccountFilter(accountObj.fields.accountNumber));dispatch(setCommissionFilter(false))}}><a >{accountObj.fields.type}</a></button></h2>
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
        </div>
    )
}

export default Account