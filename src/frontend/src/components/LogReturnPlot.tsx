import { Line } from "react-chartjs-2"
import { useFetch } from "../hook/useFetch"
import type { LogReturn } from "../types/logreturn"
import Loading from "./Loading"
import { useEffect, useRef, useState, type FC } from "react"
type LogReturnPlotProps={
    startDate?:string,
    endDate?:string
}
const LogReturnPlot:FC<LogReturnPlotProps> = ({startDate, endDate}) => {
    const [query, setQuery] = useState('log_returns');
    const { isLoading, data } = useFetch<LogReturn[]>(query);
    const chartRef = useRef(null)
    useEffect(()=>{
        let newStartDate = startDate;
        let newEndDate = endDate
        if(startDate!='' && endDate == '')
        {
            newEndDate = '2022-11-14';
        }else if(endDate != '' && startDate == ''){
            newStartDate = '1987-05-21'
        }
        if(newStartDate != '' && newEndDate != ''){
            setQuery(`log_returns?start_date='${newStartDate}'&end_date='${newEndDate}'`)
        }

    },[startDate, endDate])

    return (
        <div>
            {
                isLoading && <Loading />
            }
            {
                data?.length > 0 && <Line redraw={true} options={{ plugins: { legend: { position: 'top' }, title: { display: true, text: "Log Return Over Time", font: { size: 25, weight: 'bold' } } } }} data={{ datasets: [{ data: data.map((d) => d.log_return),backgroundColor:'rgba(75, 192, 192, 0.6)', label: "Log return" }], labels: data.map((d) => d.date) }} ref={chartRef} />
            }
        </div>
    )
}
export default LogReturnPlot;