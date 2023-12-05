#!/usr/bin/env python3
"""Contains class for processing visitor data"""
from datetime import date
import pandas as pd


class DataHandler:
    # get zip code data (so we don't have to rebuild the df every time we call zip_code_count())
    uszips = pd.read_csv('dash_app/data/uszips.csv')

    def __init__(self, path, start_date=None, end_date=None) -> None:
        """
        Initalizes an instance of the DataHandler class.

        Parameters
        ----------
        path : str
            Filepath to a CSV file containing the data

        start_date : str (Optional)
            Starting date for the filtered dataframe, format 'YYYY-MM-DD'

        end_date : str (Optional)
            Ending date for the filtered dataframe, format 'YYYY-MM-DD'

        Returns
        -------
        None
        """

        # Create dataframe from raw data
        self.df = pd.read_csv(path)

        # Set initial start and end dates for filtered dataframe
        if start_date == None:
            self._start_date = self.df['date'].min()
        else:
            self._start_date = start_date
        if end_date == None:
            self._end_date = self.df['date'].max()
        else:
            self._end_date = end_date

        # Create date-filtered dataframe
        self.dff = self.filter_data()

        # Get stats from dff
        self._total_visitors = self.total_visitors

    # Start date getter
    @property
    def start_date(self) -> str:
        return self._start_date

    # Start date setter
    @start_date.setter
    def start_date(self, value):
        if not value:
            self._start_date = self.df['date'].min()
        else:
            self._start_date = value

    # End date getter
    @property
    def end_date(self) -> str:
        return self._end_date

    # End date setter
    @end_date.setter
    def end_date(self, value):
        if not value:
            self._end_date = self.df['date'].max()
        else:
            self._end_date = value

    @property
    def total_visitors(self) -> int:
        return self.dff[['adults', 'children', 'infants', 'seniors']].sum().sum()

    @total_visitors.setter
    def total_visitors(self, value):
        self._total_visitors = value

    def all_data(self) -> pd.DataFrame:
        """
        Returns all data as a Pandas Dataframe

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            All unfiltered data in dataframe
            columns : ',id,date,firstName,lastName,country,zipCode,adults,children,infants,seniors,email,mailingList,school'
        """
        return self.df

    def filter_data(self) -> pd.DataFrame:
        """
        Creates date-filtered dataframe

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            Data, filtered by date
            columns : ',id,date,firstName,lastName,country,zipCode,adults,children,infants,seniors,email,mailingList,school'
        """
        # filter df using mask
        mask = (self.df['date'] >= self._start_date) & (self.df['date'] <= self._end_date)
        self.dff = self.df.loc[mask]
        return self.dff
   
    def reset(self) -> None:
        """
        Resets date range to all

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._start_date = self.df['date'].min()
        self._end_date = self.df['date'].max()
        self.dff = self.df

    def zip_code_count(self) -> pd.DataFrame:
        """
        Creates table of zip codes from filtered dataframe by count, and appends coordinates

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            filtered and counted zip codes with latitude and longitude
            columns : ',zipCode,counts,lat,lgn'
        """
        # get count of zip codes from dff
        zips = self.dff.loc[self.df['zipCode'].isna() == False]['zipCode'].astype(int).value_counts().reset_index(name='counts')
        uszips = self.uszips

        for zipCode in zips['zipCode']:
            try:
                zips.loc[zips['zipCode'] == zipCode, 'lat'] = uszips.loc[
                    uszips['zip'] == zipCode]['lat'].values[0]
                zips.loc[zips['zipCode'] == zipCode, 'lng'] = uszips.loc[
                    uszips['zip'] == zipCode]['lng'].values[0]
            except Exception:
                print(f'Zip code "{zipCode}" not found in uszips database')

        return zips

    def visitor_demographics(self) -> pd.DataFrame:
        """
        Creates a dataframe of visitors by age

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            Breakdown of visitors by category
        """
        return self.dff[['adults', 'children', 'infants', 'seniors']].sum()

    def daily_total_visitor_count(self, window=None) -> pd.DataFrame:
        """
        Creates table of total visitor count by day

        Parameters
        ----------
        window : int (Optional)
            Size of window for daily visitor rolling average

        Returns
        -------
        pd.DataFrame
            table of total visitor count by day
            columns : ',date,"Daily Visitors","Visitors (Rolling)"'
        """
        df = self.dff

        # sort by date
        df = df.sort_values('date')

        # group visitors by date
        df = df[['date', 'adults', 'children', 'infants', 'seniors']].groupby('date').sum()

        # sum all visitors by date
        df = df[['adults', 'children', 'infants', 'seniors']].sum(axis=1).reset_index(name='Daily Visitors')

        # Add column for 
        if window is not None:
            df[f'Visitors (Rolling)'] = df['Daily Visitors'].rolling(window, center=True).mean()

        return df

    def date_range(self) -> int:
        """
        Gets date range in days

        Parameters
        ----------
        None

        Returns
        -------
        int
            date range in days
        """
        start = date.fromisoformat(self.start_date)
        end = date.fromisoformat(self.end_date)

        return (end - start).days
        