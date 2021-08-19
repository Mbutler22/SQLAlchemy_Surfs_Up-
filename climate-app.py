{
 "cells": [
  {
   "cell_type": "raw",
   "metadata": {},
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import datetime as dt\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "from flask import Flask, jsonify"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# create engine to hawaii.sqlite\n",
    "engine = create_engine(\"sqlite:///hawaii.sqlite\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[]"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "Base = automap_base()\n",
    "Base.prepare(engine, reflect=True)\n",
    "Base.classes.keys()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "measurement=Base.classes.measurement\n",
    "\n",
    "station=Base.classes.station"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "session= Session(engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "latestDate = (session.query(Measurement.date)\n",
    "             .order_by(Measurement.date.desc())\n",
    "              .first())\n",
    "latestDate = list(np.ravel(latestDate))[0]\n",
    "\n",
    "latestDate = dt.datetime.strptime(latestDate, '%Y-%m-%d')\n",
    "lastestDate= int(dt.datetime.strftime(latestDate, '%Y'))\n",
    "latestMonth = int(dt.datetime.strftime(latestDate, '%m'))\n",
    "latestDay = int(dt.datetime.strftime(lastestDate, '%d'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "yearBefore = dt.date(latestYear, latestMonth, latestDay) - dt.timedelta(days=365)\n",
    "yearBefore = dt.datetime.strftime(yearBefore, '%Y-%m-%d')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/\")\n",
    "def home():\n",
    "    return (f\"Welcome to Surf's Up!: Hawai'i Climate API<br/>\"\n",
    "            f\"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>\"\n",
    "            f\"Available Routes:<br/>\"\n",
    "            f\"/api/v1.0/stations ~~~~~ a list of all weather observation stations<br/>\"\n",
    "            f\"/api/v1.0/precipitaton ~~ the latest year of preceipitation data<br/>\"\n",
    "            f\"/api/v1.0/temperature ~~ the latest year of temperature data<br/>\"\n",
    "            f\"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>\"\n",
    "            f\"~~~ datesearch (yyyy-mm-dd)<br/>\"\n",
    "            f\"/api/v1.0/datesearch/2015-05-30  ~~~~~~~~~~~ low, high, and average temp for date given and each date after<br/>\"\n",
    "            f\"/api/v1.0/datesearch/2015-05-30/2016-01-30 ~~ low, high, and average temp for date given and each date up to and including end date<br/>\"\n",
    "            f\"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br/>\"\n",
    "            f\"~ data available from 2010-01-01 to 2017-08-23 ~<br/>\"\n",
    "            f\"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    results = session.query(Station.name).all()\n",
    "    all_stations = list(np.ravel(results))\n",
    "    return jsonify(all_stations)\n",
    "\n",
    "@app.route(\"/api/v1.0/precipitaton\")\n",
    "def precipitation():"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "results = (session.query(Measurement.date, Measurement.prcp, Measurement.station)\n",
    "                      .filter(Measurement.date > yearBefore)\n",
    "                      .order_by(Measurement.date)\n",
    "                      .all())\n",
    "    \n",
    "    precipData = []\n",
    "    for result in results:\n",
    "        precipDict = {result.date: result.prcp, \"Station\": result.station}\n",
    "        precipData.append(precipDict)\n",
    "\n",
    "    return jsonify(precipData)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/temperature\")\n",
    "def temperature():\n",
    "\n",
    "    results = (session.query(Measurement.date, Measurement.tobs, Measurement.station)\n",
    "                      .filter(Measurement.date > yearBefore)\n",
    "                      .order_by(Measurement.date)\n",
    "                      .all())\n",
    "\n",
    "    tempData = []\n",
    "    for result in results:\n",
    "        tempDict = {result.date: result.tobs, \"Station\": result.station}\n",
    "        tempData.append(tempDict)\n",
    "\n",
    "    return jsonify(tempData)\n",
    "\n",
    "@app.route('/api/v1.0/datesearch/<startDate>')\n",
    "def start(startDate):\n",
    "    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]\n",
    "\n",
    "    results =  (session.query(*sel)\n",
    "                       .filter(func.strftime(\"%Y-%m-%d\", Measurement.date) >= startDate)\n",
    "                       .group_by(Measurement.date)\n",
    "                       .all())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "  dates = []                       \n",
    "    for result in results:\n",
    "        date_dict = {}\n",
    "        date_dict[\"Date\"] = result[0]\n",
    "        date_dict[\"Low Temp\"] = result[1]\n",
    "        date_dict[\"Avg Temp\"] = result[2]\n",
    "        date_dict[\"High Temp\"] = result[3]\n",
    "        dates.append(date_dict)\n",
    "    return jsonify(dates)\n",
    "\n",
    "@app.route('/api/v1.0/datesearch/<startDate>/<endDate>')\n",
    "def startEnd(startDate, endDate):\n",
    "    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]\n",
    "\n",
    "    results =  (session.query(*sel)\n",
    "                       .filter(func.strftime(\"%Y-%m-%d\", Measurement.date) >= startDate)\n",
    "                       .filter(func.strftime(\"%Y-%m-%d\", Measurement.date) <= endDate)\n",
    "                       .group_by(Measurement.date)\n",
    "                       .all())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "dates = []                       \n",
    "    for result in results:\n",
    "        date_dict = {}\n",
    "        date_dict[\"Date\"] = result[0]\n",
    "        date_dict[\"Low Temp\"] = result[1]\n",
    "        date_dict[\"Avg Temp\"] = result[2]\n",
    "        date_dict[\"High Temp\"] = result[3]\n",
    "        dates.append(date_dict)\n",
    "    return jsonify(dates)\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
