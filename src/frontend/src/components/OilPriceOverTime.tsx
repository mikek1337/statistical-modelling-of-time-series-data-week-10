import { Line } from "react-chartjs-2";
import { useFetch } from "../hook/useFetch"
import type { OilPrice } from "../types/oliprice"
import Loading from "./Loading";
import { useEffect, useRef, useState, type FC } from "react";
import { Chart as ChartJS, CategoryScale, LinearScale, LineElement, Title, Tooltip, Legend, PointElement } from 'chart.js'
type OilPriceOverTimeProps = {
    startDate?: string,
    endDate?: string
}
const OilPriceOverTime: FC<OilPriceOverTimeProps> = ({ startDate, endDate }) => {
    const [query, setQuery] = useState("oil_prices");
    const { isLoading, data } = useFetch<OilPrice[]>(query);
    ChartJS.register(
        CategoryScale,
        LinearScale,
        LineElement,
        PointElement,
        Title,
        Tooltip,
        Legend
    );
    useEffect(() => {
        let newStartDate = startDate;
        let newEndDate = endDate
        if (startDate != '' && endDate == '') {
            newEndDate = '2022-11-14';
        } else if (endDate != '' && startDate == '') {
            newStartDate = '1987-05-21'
        }
        if (newStartDate != '' && newEndDate != '') {
            setQuery(`oil_prices?start_date='${newStartDate}'&end_date='${newEndDate}'`)
        }
    }, [startDate, endDate])
    const chartRef = useRef(null)

    return (
        <div className="max-w-full">
            {
                isLoading && <Loading />
            }
            {
                data?.length > 0 && <Line  options={{ plugins: { legend: { position: 'top' }, title: { display: true, text: "Brent Oil Price Over Time", font: { size: 25, weight: 'bold' } } } }} data={{ datasets: [{ data: data.map((d) => d.price), label: "Price" ,backgroundColor: 'rgba(75, 192, 192, 0.6)',showLine:true}], labels: data.map((d) => d.date) }} ref={chartRef} />
            }
        </div>
    )
}

export default OilPriceOverTime;