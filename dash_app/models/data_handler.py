#!/usr/bin/env python3
"""Contains class for processing visitor data"""
import firebase_admin
import pandas as pd

from datetime import date
from firebase_admin import credentials
from google.cloud import firestore


class DataHandler:
    # get zip code data (so we don't have to rebuild the df every time we call zip_code_count())
    uszips = pd.read_csv('dash_app/data/uszips.csv')

    def __init__(self, start_date=None, end_date=None) -> None:
        """
        Initalizes an instance of the DataHandler class.

        Parameters
        ----------
        start_date : str (Optional)
            Starting date for the filtered dataframe, format 'YYYY-MM-DD'

        end_date : str (Optional)
            Ending date for the filtered dataframe, format 'YYYY-MM-DD'

        Returns
        -------
        None
        """
        # Initialize Firebase
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
        self.db = firestore.Client(project='tasm-visitor-signin')
        self.visitor_collection_ref = self.db.collection('visitors')
        self.group_collection_ref = self.db.collection('groups')

        # Initialize dataframes
        self.visitor_df = self.get_firestore_data(self.visitor_collection_ref)
        self.group_df = self.get_firestore_data(self.group_collection_ref)

        self.start_listening()

        # Set initial start and end dates for filtered dataframe
        if start_date == None:
            self._start_date = min(self.visitor_df['date'].min(), self.group_df['date'].min())
        else:
            self._start_date = start_date
        if end_date == None:
            self._end_date = max(self.visitor_df['date'].max(), self.group_df['date'].max())
        else:
            self._end_date = end_date

        # Create date-filtered dataframe
        self.visitor_dff = None
        self.group_dff = None
        self.filter_data()

        # Get stats from dff
        self._visitor_totals = self.visitor_totals
        self._group_totals = self.group_totals

    # Firebase method
    def on_snapshot(self, doc_snapshot, changes, read_time):
        data_list = []

        for doc in doc_snapshot:
            if doc.exists:
                # Check the collection from which the document originates
                if 'visitors' in doc.reference.path:
                    data_list.append(doc.to_dict())
                elif 'groups' in doc.reference.path:
                    data_list.append(doc.to_dict())

        if data_list:
            if 'visitors' in doc.reference.path:
                self.visitor_df = pd.DataFrame(data_list)
                self.filter_data()
            elif 'groups' in doc.reference.path:
                self.group_df = pd.DataFrame(data_list)
                self.filter_data()

    # Firebase method
    def get_firestore_data(self, collection_ref):
        data_list = []
        docs = collection_ref.stream()

        for doc in docs:
            if doc.exists:
                data_list.append(doc.to_dict())

        return pd.DataFrame(data_list)

    # Firebase method
    def start_listening(self):
        # Watch the collection for changes
        self.visitor_doc_watch = self.visitor_collection_ref.on_snapshot(self.on_snapshot)
        self.group_doc_watch = self.group_collection_ref.on_snapshot(self.on_snapshot)

    # Firebase method
    def stop_listening(self):
        # Stop watching for changes
        self.visitor_doc_watch.unsubscribe()
        self.group_doc_watch.unsubscribe()

    # Start date getter
    @property
    def start_date(self) -> str:
        return self._start_date

    # Start date setter
    @start_date.setter
    def start_date(self, value):
        if not value:
            self._start_date = min(self.visitor_df['date'].min(), self.group_df['date'].min())
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
            self._end_date = max(self.visitor_df['date'].max(), self.group_df['date'].max())
        else:
            self._end_date = value

    # visitor_totals getter
    @property
    def visitor_totals(self) -> int:
        return self.visitor_dff[['adults', 'students', 'kids', 'seniors']].sum().sum()

    # visitor_totals setter
    @visitor_totals.setter
    def visitor_totals(self, value):
        self._visitor_totals = value

    # group_totals getter
    @property
    def group_totals(self) -> int:
        return self.group_dff[['adults', 'students']].sum().sum()

    # group_totals setter
    @group_totals.setter
    def group_totals(self, value):
        self._group_totals = value

    def visitor_data(self) -> pd.DataFrame:
        """
        Returns visitor data as a Pandas Dataframe

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            All unfiltered data in dataframe
        """
        return self.visitor_df

    def group_data(self) -> pd.DataFrame:
        """
        Returns group data as a Pandas Dataframe

        Parameters
        ----------
        None

        Returns
        -------
        pd.DataFrame
            All unfiltered data in dataframe
        """
        return self.group_df

    def filter_data(self) -> pd.DataFrame:
        """
        Creates date-filtered dataframe

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe to filter

        Returns
        -------
        pd.DataFrame
            Dataframe filtered by date
        """
        # filter df using mask
        visitor_mask = (self.visitor_df['date'] >= self._start_date) & (self.visitor_df['date'] <= self._end_date)
        self.visitor_dff = self.visitor_df.loc[visitor_mask]
        group_mask = (self.group_df['date'] >= self._start_date) & (self.group_df['date'] <= self._end_date)
        self.group_dff = self.group_df.loc[group_mask]

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
        self._start_date = min(self.visitor_df['date'].min(), self.group_df['date'].min())
        self._end_date = max(self.visitor_df['date'].max(), self.group_df['date'].max())
        self.visitor_dff = self.visitor_df
        self.group_dff = self.group_df

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
        # Get zip columns
        visitor_zips = self.visitor_dff['zip']
        group_zips = self.group_dff['zip']

        # Create a list of all zips
        all_zips = pd.concat([visitor_zips, group_zips], axis=0, ignore_index=True).to_frame()

        # get count of zip codes
        zips = all_zips.loc[all_zips['zip'].isna() == False]['zip'].astype(int).value_counts().reset_index(name='counts')
        uszips = self.uszips

        for zipCode in zips['zip']:
            try:
                zips.loc[zips['zip'] == zipCode, 'lat'] = uszips.loc[
                    uszips['zip'] == zipCode]['lat'].values[0]
                zips.loc[zips['zip'] == zipCode, 'lng'] = uszips.loc[
                    uszips['zip'] == zipCode]['lng'].values[0]
            except Exception:
                pass

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
        df = self.visitor_dff[['adults', 'students', 'kids', 'seniors']].sum()
        df['adults'] += self.group_dff['students'].sum()
        df['students'] += self.group_dff['adults'].sum()

        return df

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
            df of total visitor count by day
        """
        vdf = self.visitor_dff
        gdf = self.group_dff

        # sort by date
        vdf = vdf.sort_values('date')
        gdf = gdf.sort_values('date')

        # group visitors by date
        vdf = vdf[['date', 'adults', 'kids', 'students', 'seniors']].groupby('date').sum()
        gdf = gdf[['date', 'adults', 'students']].groupby('date').sum()

        # sum all visitors by date
        vdf = vdf[['adults', 'kids', 'students', 'seniors']].sum(axis=1).reset_index(name='Non-School Visitors')
        gdf = gdf[['adults', 'students']].sum(axis=1).reset_index(name='School Group Visitors')

        # Add column for rolling avg
        if window is not None:
            vdf['Visitor Avg (2wks)'] = vdf['Non-School Visitors'].rolling(window, center=True).mean()
            gdf['Group Avg (2wks)'] = gdf['School Group Visitors'].rolling(window, center=True).mean()

        return vdf.merge(gdf, how='outer').fillna(0)

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
