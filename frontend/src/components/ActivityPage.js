import React, { useEffect,useState } from "react";
import { useSelector } from 'react-redux';

import { DataGrid } from '@mui/x-data-grid';
import { Box, Paper } from "@mui/material";

    
const ActivityPage = () => {

    const [activities, setActivities] = useState([])
    console.log("STATE")
    console.log(useSelector((state) => state))
    const isCommission = useSelector((state) => state.commission.value)
    const isDeposit = useSelector((state) => state.deposits.value)
    const isTrades = useSelector((state) => state.trades.value)
    const accountFilter = useSelector((state) => state.accountFilter.value)
    let fetchUrl = 'http://localhost:8000/api/activity';
    let commissionUrl = 'http://localhost:8000/api/account/commission';

    const columns = [
        { field: 'symbol', headerName: 'Symbol', width: 70 },
        { field: 'currency', headerName: 'Currency', width: 130 },
        { field: 'price', headerName: 'Price', width: 130 },
        { field: 'type', headerName: 'Type', width: 130 },
        { field: 'quantity', headerName: 'Quantity', width: 130 },
        { field: 'commission', headerName: 'Commission', width: 130 },
        { field: 'netAmount', headerName: 'Net Amount', width: 130 },
        { field: 'grossAmount', headerName: 'Gross Amount', width: 130 }
      ];

    if (accountFilter.length > 0 && (isCommission == false)) {

        fetchUrl = fetchUrl + '?accountNumber=' + accountFilter
    }
        

    const setFetchURl = (url, params) => {

    }
    useEffect (() => {
        fetch(fetchUrl)
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            setActivities(data.activities);
        })
    }, [isCommission, accountFilter])
    
    const getRowsData  = () => {
  
        const rows = activities.map((activity, indx) => {
            return {
                "id": indx,
                "symbol" : activity.fields.symbol,
                "currency" : activity.fields.currency,
                "price" : activity.fields.price,
                "type" : activity.fields.type,
                "quantity" : activity.fields.quantity,
                "commission" : activity.fields.commission,
                "netAmount" : activity.fields.netAmount,
                "grossAmount" : activity.fields.grossAmount
            }
        })
        return rows;
    }
    return (
        <Box style={{  marginTop: 20, height: 400, width: '100%' }}>
            <Paper>
                <DataGrid
                rowSelection={false}
                rows={getRowsData()}
                columns={columns}
                initialState={{
                pagination: {
                    paginationModel: { page: 0, pageSize: 10 },
                },
                }}
                pageSizeOptions={[10, 20]}
                checkboxSelection
                />
            </Paper>
            
        </Box>
    )
}

export default ActivityPage