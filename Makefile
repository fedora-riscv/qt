# Makefile for source rpm: qt
# $Id$
NAME := qt
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
