import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import moment from "moment";
import { DataGrid } from "@mui/x-data-grid";
import { Box, Paper } from "@mui/material";
import Filters from "../Filters";

const ActivityPage = () => {
  const [activities, setActivities] = useState([]);
  const accountFilterState = useSelector((state) => state.accountFilter.value);
  const activityTypeFilterState = useSelector(
    (state) => state.activityTypeFilters.value
  );

  let fetchUrl = new URL("http://localhost:8000/api/activity");

  const activityTypes = [
    { label: "Trades" },
    { label: "Dividends" },
    { label: "Deposits" },
    { label: "FX conversion" },
  ];
  const columns = [
    { field: "account_number", headerName: "Acc Number", minWidth: 100 },
    { field: "symbol", headerName: "Symbol", minWidth: 70 },
    { field: "currency", headerName: "Currency", minWidth: 50 },
    { field: "price", headerName: "Price", minWidth: 70 },
    { field: "type", headerName: "Type", minWidth: 90 },
    { field: "quantity", headerName: "Quantity", minWidth: 50 },
    { field: "commission", headerName: "Commission", minWidth: 70 },
    { field: "netAmount", headerName: "Net Amount", minWidth: 100 },
    { field: "tradeDate", headerName: "Trade Date", minWidth: 150, flex: 1 },
  ];

  const setFetchURl = () => {
    if (accountFilterState.length > 0)
      fetchUrl.searchParams.append("account", accountFilterState);
    if (activityTypeFilterState.length > 0)
      fetchUrl.searchParams.append("activityType", activityTypeFilterState);
    return fetchUrl;
  };

  useEffect(() => {
    setFetchURl();
    fetch(fetchUrl)
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        setActivities(data.activities);
      });
  }, [accountFilterState, activityTypeFilterState]);

  const getRowsData = () => {
    const rows = activities.map((activity, indx) => {
      return {
        id: indx,
        account_number: activity.account_number,
        symbol: activity.symbol,
        currency: activity.currency,
        price: activity.price,
        type: activity.type,
        quantity: activity.quantity,
        commission: activity.commission,
        netAmount: activity.net_amount,
        grossAmount: activity.gross_amount,
        tradeDate: moment(activity.trade_date).format("DD/MM/YYYY"),
      };
    });
    return rows;
  };
  return (
    <div>
      <Filters activityTypes={activityTypes} />
      <Box style={{ marginTop: 20, height: 400, width: "100%" }}>
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
    </div>
  );
};

export default ActivityPage;
