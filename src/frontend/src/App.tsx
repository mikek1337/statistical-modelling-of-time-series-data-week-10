import { useState} from "react"
import OilPriceOverTime from "./components/OilPriceOverTime";
import LogReturnPlot from "./components/LogReturnPlot";
import { X } from "lucide-react";
import ChangePointSummary from "./components/ChangePointSummary";

function App() {
  
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const clearFilter = ()=>{
   
      setStartDate('')
      setEndDate('')
    
  }

  return (
    <>
      <div className="max-w-[80%] mx-auto my-2 bg-zinc-300 text-zinc-600 p-10">
        <div className="mx-auto text-center">
          <h1 className="font-bold text-5xl text-zinc-600">Brent Oil Price Analysis Dashboard</h1>
          <p className="text-gray-500 font-semibold">insight from Bayesain Change Point Detection and Time series analysis</p>
        </div>
        <div className="flex justify-center-safe my-10 items-start gap-5 w-full">
          <div className="flex flex-col gap-2">
            <label>Start date</label>
            <input type="date" min={'1987-05-21'} max={endDate || '2022-11-14'} className="w-full border border-zinc-300 rounded-md p-3" onChange={(e)=>setStartDate(e.target.value)} value={startDate}/>
          </div>
          <div className="flex flex-col gap-2">
            <label>End date</label>
            <input type="date" min={startDate || '1987-05-21'} max={'2022-11-14'} className="w-full  border border-zinc-300 rounded-md p-3" onChange={(e)=>setEndDate(e.target.value)} value={endDate}/>
          </div>
          <div>
            {
              (startDate != '' || endDate != '') &&
              <button className="bg-red-500 text-white p-2 font-semibold rounded-md w-full px-10 flex gap-2 items-center" onClick={clearFilter}>
                <X className="w-5 h-5"/>
                Clear Filter
              </button>
            }
          </div>
        </div>
        <div className="grid md:grid-cols-2 grid-cols-1 gap-2 mt-10 ">
          
          {/* { oilData !==undefined && <Line datasetIdKey="date" data={{
              labels:["Date", "Price"],
              datasets:oilData
          }} ref={chartRef}/>} */}
          <OilPriceOverTime startDate={startDate} endDate={endDate}/>
          <LogReturnPlot startDate={startDate} endDate={endDate}/>
          <ChangePointSummary/>
        </div>
      </div>
   </>
  )
}

export default App
