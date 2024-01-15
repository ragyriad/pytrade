import React from "react";


const Header = () => {
    const container = {
        border: "0.05em solid red",
        width:"100%",
        display: "flex",
        justifyContent: "center"
    }
    return (
        <div style={{
            display: "flex",
            justifyContent: "center"
        }}>
            <h1>PyTrade</h1>
        </div>
         
    )
}

export default Header