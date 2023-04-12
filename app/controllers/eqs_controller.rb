class EqsController < ApplicationController
  def index
    @eqs = Eq.all
  end
end
