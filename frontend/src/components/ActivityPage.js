import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";

import { DataGrid } from "@mui/x-data-grid";
import { Box, Paper } from "@mui/material";

import Filters from "./Filters";

const ActivityPage = () => {
  console.log("STATE");
  console.log(useSelector((state) => state));
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
  ];
  const isCommission = false;

  const columns = [
    { field: "symbol", headerName: "Symbol", width: 70 },
    { field: "currency", headerName: "Currency", width: 130 },
    { field: "price", headerName: "Price", width: 130 },
    { field: "type", headerName: "Type", width: 130 },
    { field: "quantity", headerName: "Quantity", width: 130 },
    { field: "commission", headerName: "Commission", width: 130 },
    { field: "netAmount", headerName: "Net Amount", width: 130 },
    { field: "grossAmount", headerName: "Gross Amount", width: 130 },
  ];

  const setFetchURl = () => {
    if (accountFilterState.length > 0)
      fetchUrl.searchParams.append("account", accountFilterState);
    if (activityTypeFilterState.length > 0)
      fetchUrl.searchParams.append("activityType", activityTypeFilterState);
    console.log(fetchUrl.href);
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
        symbol: activity.fields.symbol,
        currency: activity.fields.currency,
        price: activity.fields.price,
        type: activity.fields.type,
        quantity: activity.fields.quantity,
        commission: activity.fields.commission,
        netAmount: activity.fields.netAmount,
        grossAmount: activity.fields.grossAmount,
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
