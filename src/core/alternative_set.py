from sqlalchemy import *
import os
import sys

class AlternativeSet(object):
	"""Represents a set of alternatives.
	"""
	def __init__(self, name, metadata):
		"""altern_set = AlternativeSet(string, BoundMetadata)
		
		name - name of alternative set and ultimately the underlying DB table
		metadata - SQLAlchemy metadata object providing access to DB engine and tables
		"""
		self.name = name
		self.metadata = metadata
		self.table = None
		self.mapper = None
		
		#Load alternative table from DB if it exists otherwise create it
		if self.metadata.engine.has_table(self.name):
			self.table = Table(self.name, self.metadata, autoload=True)
		else:
			self.__create_alternative_table()
		
		#Map Alternative object to alternative table
		self.mapper = mapper(Alternative, self.table)
		
		#print list(self.table.columns)

	def __create_alternative_table(self):
		"""Create a new alternative table in the DB
		"""
		self.table = self.__get_alternative_table_object()
		self.table.create()
	
	def __get_alternative_table_object(self):
		"""Create alternative Table object (SQLAlchemy)
		"""
		print "returning table object"
		return Table(self.name, self.metadata,
			Column('alternative_id', Integer, Sequence('altern_id_seq'), primary_key=True),
			Column('name', String(200))
		)
		
	def add_alternative(self, name):
		"""Add alternative to the AlternativeSet
		
		name (string) - name of the alternative
		"""
		self.table.insert().execute({'name':name})
	
	def remove_alternative(self, alternative_id):
		"""Remove alternative from AlternativeSet given its unique alternative id
		"""
		result = self.table.delete(self.table.c.alternative_id==alternative_id).execute()
		#TODO : verify this is True
		return True

	def get_alternative_ids(self):
		"""Returns list of IDs of alternatives currently loaded
		"""
		altern_id_list = []
		for row in self.table.select(order_by=self.table.c.alternative_id).execute():
			altern_id_list.append(row.alternative_id)
		return altern_id_list
	
	def get_num(self):
		"""Returns the number of alternatives stored in the AlternativeSet
		"""
		session = create_session(bind_to=self.metadata.engine)
		return int(session.query(self.mapper).count())

	def __unicode__(self):
		"""Description of object
		"""
		return "AlternativeSet"
	
	def __str__(self):
		"""Description of object
		"""
		return "AlternativeSet"
	
	def to_string(self):
		"""Returns string representation of the AlternativeSet
		"""
		i = self.table.select().execute()
		ir = i.fetchall()
		altern_str = ""
		for row in ir:
			altern_str += str(row)+"\n"
		if altern_str == "":
			altern_str = "No alternatives defined"
		return altern_str

class Alternative(object):
	"""Alternative class maps to alternative DB tables allowing access to them in OO way using SQLAlchemy
	
	Members for this class are created dynamically by SQLAlchemy at the time of mapping.  Member
	names correspond directly to names of attributes in the table mapped to.
	"""
	pass
	
#Testing purposes
if __name__ == '__main__':
 	os.chdir('..')	#Go to top-level directory
	db = create_engine('sqlite:///db/project23.del')
	meta = BoundMetaData(db)	#Basically a schema, or table collection
	altern_set = AlternativeSet('alternatives', meta)
	altern_set.add_alternative("testy")
	print altern_set.to_string()