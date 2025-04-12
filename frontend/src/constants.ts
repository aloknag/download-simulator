// Read environment variable PROD=true and set accordingly.
const isProd = import.meta.env.PROD

const API_SERVER_URL = isProd
  ? '' // production URL is same as web URL
  : 'http://localhost:5000'

export default API_SERVER_URL
