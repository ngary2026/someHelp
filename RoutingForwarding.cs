using System;
using System.Collections.Generic;
using System.Text;

namespace ChpFour
{
    class RouterForwarding
    {
        static List<List<RouterDataRow>> inputPorts = new List<List<RouterDataRow>>()
        {
            new List<RouterDataRow>(),
            new List<RouterDataRow>(),
            new List<RouterDataRow>()
        };

        // The latest time that a packet entered this port.
        static List<double> outputPortLastBusTime = new List<double>()
        {
            0,
            0,
            0
        };
        // The latest time that a packet left this port.
        static List<double> outputPortLastTransmitTime = new List<double>()
        {
            0,
            0,
            0
        };

        static double latestBusTransmitTime = -1;
        static int lastCheckedPort = -1;

        public static void Process(double packetTransmitTime, double outputTransmitTime, List<RouterDataRow> table)
        {
            double memoryResult = 0;
            Cleanup(ref table);
            memoryResult = Run(packetTransmitTime*2.0, outputTransmitTime);
            Cleanup(ref table);
            double busResult = Run(packetTransmitTime, outputTransmitTime);
            Cleanup(ref table);
            double crossbarResult = RunCrossbar(packetTransmitTime, outputTransmitTime);

            Console.WriteLine($"Router Forwarding:{memoryResult},{busResult},{crossbarResult}");
        }

        private static double Run(double packetTransmitTime, double outputTransmitTime)
        {
            // While packets still in input ports.
            while (inputPorts[0].Count > 0 || inputPorts[1].Count > 0 || inputPorts[2].Count > 0)
            {
                // Round Robin input port checking, so we want to start at the port after the last checked.
                int startInput = (lastCheckedPort + 1) % 3;
                lastCheckedPort = startInput;
                // Find next earliest packet.
                // The first time we do this, we don't care about bus time, just the first input avaliable. 
                // After that, the packets available are all that have arrived before the latest bus transmission time.
                int rdr = latestBusTransmitTime == -1 ? GetNextInputNoWait(startInput) : GetNextInput(startInput, latestBusTransmitTime);

                // This is the time that the packet is finished transmitting across the bus.
                double inputTime = Math.Max(inputPorts[rdr][0].arrivalTime, latestBusTransmitTime) + packetTransmitTime;
                // Packet can only propagate after the last packet in the output has finished propagating.
                double propagateTime = Math.Max(inputTime, outputPortLastTransmitTime[inputPorts[rdr][0].outputPort - 1])
                    + outputTransmitTime;

                // Set output information.
                outputPortLastBusTime[inputPorts[rdr][0].outputPort - 1] = Math.Round(inputTime, 1);
                outputPortLastTransmitTime[inputPorts[rdr][0].outputPort - 1] = Math.Round(propagateTime, 1);
                // Latest time that the bus was free.
                latestBusTransmitTime = Math.Round(inputTime, 1);

                lastCheckedPort = rdr;
                // Remove packet from input port.
                inputPorts[rdr].RemoveAt(0);
            }

            return GetResult();
        }

        private static double RunCrossbar(double packetTransmitTime, double outputTransmitTime)
        {
            // While packets still in input ports.
            while (inputPorts[0].Count > 0 || inputPorts[1].Count > 0 || inputPorts[2].Count > 0)
            {
                // Round Robin input port checking, so we want to start at the port after the last checked.
                int startInput = (lastCheckedPort + 1) % 3;
                lastCheckedPort = startInput;
                // Find next earliest packet.
                int rdr = GetNextInputNoWait(startInput);
                // This is the time that the packet is finished transmitting across the bus.
                double inputTime = inputPorts[rdr][0].arrivalTime + packetTransmitTime;
                // If the bus is busy, can't transmit until it's not.
                if (inputPorts[rdr][0].arrivalTime < outputPortLastBusTime[rdr])
                {
                    inputTime = outputPortLastBusTime[rdr] + packetTransmitTime;
                }
                // Packet can only propagate after the last packet has finished propagating.
                double propagateTime = Math.Max(inputTime, outputPortLastTransmitTime[inputPorts[rdr][0].outputPort - 1])
                    + (outputTransmitTime);
                // Set the packet as the latest in the port.
                outputPortLastBusTime[inputPorts[rdr][0].outputPort - 1] = Math.Round(inputTime, 1);
                outputPortLastTransmitTime[inputPorts[rdr][0].outputPort - 1] = Math.Round(propagateTime, 1);
                // Latest time that the bus was free.
                latestBusTransmitTime = inputTime;

                // Remove packet from input port.
                inputPorts[rdr].RemoveAt(0);
            }

            return GetResult();
        }

        private static int GetNextInput(int startIndex, double checkTime)
        {
            int leastTimeIndex = -1;
            for(int i = 0; i < 3; i++)
            {
                int realIndex = (startIndex + i) % 3;
                if (inputPorts[realIndex].Count > 0)
                {
                    // There are no packets in this port.
                    if(inputPorts[realIndex].Count == 0)
                    {
                        continue;
                    }
                    // Find the first packet in order that has arrived.
                    if (inputPorts[realIndex][0].arrivalTime
                        <= checkTime)
                    {
                        leastTimeIndex = realIndex;
                        lastCheckedPort = leastTimeIndex;
                        return leastTimeIndex;
                    }
                }
            }
            if(leastTimeIndex == -1)
            {
                return GetNextInputNoWait(startIndex);
            }
            return leastTimeIndex;
        }

        private static int GetNextInputNoWait(int startIndex)
        {
            int leastTimeIndex = -1;
            double earliestArrival = double.MaxValue;
            for (int i = 0; i < 3; i++)
            {
                int realIndex = (startIndex + i) % 3;
                if (inputPorts[realIndex].Count > 0)
                {
                    // There are no packets in this port.
                    if (inputPorts[realIndex].Count == 0)
                    {
                        continue;
                    }
                    // Find the first packet in order that has arrived.
                    if (inputPorts[realIndex][0].arrivalTime
                        < earliestArrival)
                    {
                        leastTimeIndex = realIndex;
                        earliestArrival = inputPorts[realIndex][0].arrivalTime;
                        lastCheckedPort = leastTimeIndex;
                    }
                }
            }
            return leastTimeIndex;
        }


        private static void Cleanup(ref List<RouterDataRow> table)
        {
            inputPorts = new List<List<RouterDataRow>>()
            {
                new List<RouterDataRow>(),
                new List<RouterDataRow>(),
                new List<RouterDataRow>()
            };
            /*outputPorts = new List<RouterOutputPort>()
            {
                null,
                null,
                null
            };*/
            outputPortLastBusTime = new List<double>()
            {
                0,
                0,
                0
            };
            outputPortLastTransmitTime = new List<double>()
            {
                0,
                0,
                0
            };
            latestBusTransmitTime = -1;
            lastCheckedPort = -1;

            // Fill input ports.
            for (int i = 0; i < table.Count; i++)
            {
                switch (table[i].inputPort)
                {
                    case 1:
                        inputPorts[0].Add(table[i]);
                        break;
                    case 2:
                        inputPorts[1].Add(table[i]);
                        break;
                    case 3:
                        inputPorts[2].Add(table[i]);
                        break;
                }
            }
        }

        private static double GetResult()
        {
            double largest = outputPortLastTransmitTime[0];
            for (int i = 0; i < outputPortLastTransmitTime.Count; i++)
            {
                if (outputPortLastTransmitTime[i] > largest)
                {
                    largest = outputPortLastTransmitTime[i];
                }
            }
            return largest;
        }
    }
}
