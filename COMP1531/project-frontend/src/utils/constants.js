require("dotenv").config();

export const drawerWidth = 240;
const port = window.BACKEND_PORT;
const local = window.LOCAL_ENV || false;
console.log(local)
export const url = port === 0 || !local ? "https://flockr-be.herokuapp.com" : "http://localhost:" + port;

export const PERMISSION_IDS = {
  OWNER: 1,
  MEMBER: 2
};
export const PAGINATION_SIZE = 50;
export const SLICE_SIZE = 10;
