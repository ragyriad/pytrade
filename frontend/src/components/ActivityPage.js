import React, { useEffect,useState } from "react";
import { useSelector } from 'react-redux'
    
    
const ActivityPage = (accountNumberFilter) => {

    const [activities, setActivities] = useState([])
    const state = useSelector((state) => state)
    console.log(state)
    const isCommission = useSelector((state) => state.commissionFilter.value)
    const accountFilter = useSelector((state) => state.accountFilter.value)
    let fetchUrl = 'http://localhost:8000/api/activity';
    let commissionUrl = 'http://localhost:8000/api/account/commission';
    if (accountFilter != 0 && (isCommission == false)) {

        fetchUrl = fetchUrl + '?accountNumber=' + accountFilter
    }
        
    else if(isCommission)
        fetchUrl = commissionUrl

    useEffect (() => {
        fetch(fetchUrl)
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            console.log(data);
            setActivities(data.activities);
        })
    }, [accountNumberFilter, isCommission, accountFilter])

    return (
        <div style={{
            display: "flex",
            justifyContent: "center"
        }}>
            <table>
                <thead>
                    <tr>
                        <th>symbol</th>
                        <th>currency</th>
                        <th>price</th>
                        <th>type</th>
                        <th>quantity</th>
                        <th>comission</th>
                        <th>net Amount</th>
                        <th>Gross Amount</th>
                    </tr>
                </thead>
                <tbody>
            {activities.map((activity) => {
                return (
                    <tr>
                        <td>{activity.fields.symbol}</td>
                        <td>{activity.fields.currency}</td>
                        <td>{activity.fields.price}</td>
                        <td>{activity.fields.type}</td>
                        <td>{activity.fields.quantity}</td>
                        <td>{activity.fields.commission}</td>
                        <td>{activity.fields.netAmount}</td>
                        <td>{activity.fields.grossAmount}</td>
                    </tr>
                )
            })}
                </tbody>
            </table>
        </div>
        
    )
}

export default ActivityPage